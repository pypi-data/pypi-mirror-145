"""Base implementation for device drivers"""
import abc
import asyncio
import json
import logging

from flask import Flask, current_app, make_response, request, jsonify

from shifu_driver import schema, watchdog, socket_backend, driver_bp


def route(route, endpoint=None, methods=['POST']):
    def wrapped_f(func):
        func.__route__ = route
        func.__endpoint__ = endpoint
        func.__methods__ = methods
        return func

    return wrapped_f


def is_route(func):
    return hasattr(func, '__route__') and hasattr(func, '__methods__')


def view_func_wrapper(func):
    def view_func():
        json_dict = request.get_json(silent=True) or {}
        return func(**json_dict)

    return view_func


class ShifuDriver(abc.ABC, Flask):
    def __init__(self):
        super().__init__(__name__)

        # Start logging
        self.logger = logging.getLogger(__name__)

        # Set asyncio event loop
        self.event_loop = asyncio.get_event_loop()

        # Create device state attributes
        self.device_status = schema.DeviceStatus()
        self.connection_status = schema.ConnectionStatus()

        # # Override self.connect in child classes in needed
        self.initialized = False

        driver_bp.before_request_funcs.setdefault(None, []).append(self.check_device_initialization)
        for attr in dir(self):
            field = getattr(self, attr)
            if callable(field) and is_route(field):
                driver_bp.add_url_rule(
                    field.__route__,
                    field.__endpoint__ or '-'.join(field.__qualname__.split('.')),
                    view_func_wrapper(field),
                    methods=field.__methods__,
                )

        self.register_blueprint(driver_bp)

    def __del__(self):
        if self.initialized:
            self.disconnect()
            self.watchdog.stop()

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        super().run(host, port, debug, load_dotenv, **options)

    def check_device_initialization(self):
        if not self.initialized and (
            request.endpoint not in ['driver.ShifuDriver-initialize_device', 'driver.ShifuDriver-_endpoints']
        ):
            return "Device not initialized"

    @route('/initialize', methods=['POST'])
    def initialize_device(self, **kwargs):
        self.device_config = schema.Config.from_json(kwargs)
        self.com_backend = self.connect()
        self.watchdog = watchdog.Watchdog(
            self.send_heartbeat, self.connection_status, self.device_config, self.event_loop
        )
        self.watchdog.start()
        self.initialized = True
        return make_response("Initialization Success!")

    @route('/endpoints', methods=['GET'])
    def _endpoints(self):
        url_map = current_app.url_map

        device_endpoints = []
        for rule in url_map._rules:
            device_endpoint = {'rule': rule.rule, 'endpoint': rule.endpoint, 'methods': list(rule.methods)}
            device_endpoint['view_func'] = current_app.view_functions[device_endpoint['endpoint']].__qualname__
            device_endpoints.append(device_endpoint)

        return jsonify(device_endpoints)

    # TODO: refactor according to current config,
    # TODO: connection_info should be from a different source if com_backend is not used
    def to_dict(self):
        data = {'connection_info': self.connection_status.to_dict(), 'device_info': self.device_status.to_dict()}
        return data

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        return f"<{type(self).__name__} ({self.__class__!r})>"

    # ############ Standard device functions ############ #

    # Externally accessible connect method
    def connect(self):
        com_backend = socket_backend.SocketBackend(
            self.connection_status, self.device_config, self.socket_response_processor, self.event_loop
        )
        asyncio.run_coroutine_threadsafe(
            com_backend.create_connection(self.device_config.device_ip, self.device_config.device_port), self.event_loop
        )
        return com_backend

    # Externally accessible disconnect method
    def disconnect(self):
        asyncio.run_coroutine_threadsafe(self.com_backend.destroy_connection(), self.event_loop)

    @abc.abstractmethod
    def send_heartbeat(self, timeout):
        """
        Driver instances must override this method.
        For blocking heartbeat calls, call self.watchdog.feed_watchdog() on success and respect the timeout.
        """
        raise NotImplementedError

    # TODO: implement the following functions later
    # @abc.abstractmethod
    # def sync_state(self):
    #     """
    #     Function to synchronize state before command.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def check_idle(self):
    #     """
    #     Decorator to check whether the state is idle before command.
    #     """
    #     raise NotImplementedError

    # def socket_response_processor(self, message):
    #     """
    #     Driver instances that use socket communication backend must override this method.
    #     For nonblocking heartbeat calls, call self.watchdog.feed_watchdog() here.
    #     """
    #     raise NotImplementedError
