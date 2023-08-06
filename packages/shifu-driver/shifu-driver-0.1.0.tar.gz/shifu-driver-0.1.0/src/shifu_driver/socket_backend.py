"""Communication base for devices"""
import asyncio
import contextlib
from datetime import datetime
import logging
import threading

from shifu_driver.schema import ConnectionState


class SocketBackend:
    def __init__(self, connection_status, device_config, message_processor, event_loop):
        # Start logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Set config and create connection state attributes
        self.config = device_config
        self.connection = connection_status

        # Set message processor for callback upon response available
        self.message_processor = message_processor

        # Set asyncio event loop
        self.event_loop = event_loop

        # Create connection-dependent variables
        self.send_queue = None
        self.response_available = threading.Event()
        self.device_tasks = set()

        # self.watchdog = watchdog.Watchdog(self.config.heartbeat_send_delay, self, None)

    async def read_handler(self, reader):
        self.logger.debug("read handler started")

        # Wait for message from device and process it
        async for message in self.read(reader):
            await asyncio.to_thread(self.message_processor, message)
            self.response_available.set()

        self.logger.debug("exiting read handler")

    async def read(self, reader):
        data_stream = b''
        try:
            while data_stream := data_stream + await reader.read(1024):
                if self.config.term_char.encode() in data_stream:
                    message, data_stream = data_stream.split(self.config.term_char.encode(), 1)
                    self.connection.packets_received += 1
                    yield message.decode()  # TODO: Handle decode error
        except ConnectionResetError:
            self.logger.warning("Connection reset")
            pass  # TODO: Handle reconnect strategy
        if data_stream:
            yield data_stream.decode()  # TODO: Handle decode error

    async def write_handler(self, writer):
        self.logger.debug("Write handler started")

        try:
            while (message := await self.send_queue.get()) != b'':
                await self.write(writer, message)
                self.send_queue.task_done()
        finally:
            self.logger.debug("Draining writer...")
            await writer.drain()
            writer.close()
            self.logger.debug("Exiting write handler")
            self.logger.info(
                "Disconnected from device uri {self.config.device_ip}:{self.config.device_port}"
            )  # noqa: E501

    async def write(self, writer, message):
        # Terminate message
        if not message.endswith(self.config.term_char):
            message += self.config.term_char

        # Write message
        writer.write(message.encode())
        await writer.drain()  # TODO: Handle broken pipe / other socket errors
        self.connection.packets_sent += 1

    async def add_to_send_queue(self, message):
        if self.send_queue:
            await self.send_queue.put(message)
        else:
            self.logger.warning(f"Send failed, device not connected: {message}")

    async def create_connection(self, host='127.0.0.1', port=9000):
        # Check if device is already connected or a connection attempt is pending
        if self.connection.state == ConnectionState.CONNECTED:
            self.logger.warning("Device already connected")
            return
        elif self.connection.state == ConnectionState.CONNECTION_IN_PROGRESS:
            self.logger.warning("Already attempting to connect to device")
            return

        # Signal that a connection attempt is in progress
        self.connection.state = ConnectionState.CONNECTION_IN_PROGRESS
        print('CONNECTION_IN_PROGRESS!!!')

        # Create asyncio queues for sending and receiving data
        self.send_queue = asyncio.Queue()  # TODO: Convert to PriorityQueue to service ESTOP first

        # Handle server configuration
        if self.config.backend_type == 'server':  # TODO: Implement server handling
            self.logger.info(f"Creating connection on {host}:{port} for device")
            self.server = await asyncio.start_server(self.set_stream_refs, host, port)
        # Handle client configuration
        else:
            self.logger.info(f"Connecting to device on {host}:{port}")
            retry_num = 0
            while retry_num < self.config.max_conn_attempts:
                try:
                    reader, writer = await asyncio.open_connection(host, port)
                    break
                except ConnectionRefusedError:
                    self.logger.warning("Failed to connect to device, retrying...")
                    retry_num += 1
                    await asyncio.sleep(2)
            # Max attempts hit, connection failed
            if retry_num >= self.config.max_conn_attempts:
                self.connection.state = ConnectionState.CONNECTION_FAILED
                self.logger.warning(f"Failed to connect to device on {host}:{port}")
                return

            # Connection was successful
            self.connection.state = ConnectionState.CONNECTED
            self.connection.start_time = datetime.now()
            self.logger.info(f"Connected to {host}:{port}")

        # Create tasks for reading from and writing to device
        read_task = asyncio.create_task(self.read_handler(reader), name='read_handler')
        write_task = asyncio.create_task(self.write_handler(writer), name='write_handler')

        # Add newly created tasks to set of device tasks
        self.device_tasks.add(read_task)
        self.device_tasks.add(write_task)

        # # Start device watchdog
        # self.watchdog.start()

    def set_stream_refs(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def destroy_connection(self):
        # Ensure device is actually connected
        if self.connection.state != ConnectionState.CONNECTED:
            self.logger.warning("Device not connected")
            return

        self.logger.info(
            f"Disconnecting from device at {self.config.device_ip}:{self.config.device_port}"
        )  # noqa: E501

        # # Stop watchdog
        # self.watchdog.stop()

        # Cancel pending device tasks
        pending_tasks = self.device_tasks.intersection(asyncio.all_tasks())

        for task in pending_tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        # Destroy queue and clear connection-associated tasks
        self.send_queue = None
        self.response_available.clear()
        self.device_tasks.clear()

        # Reset per-session connection stats
        self.connection.state = ConnectionState.DISCONNECTED
        self.connection.start_time = 0

    # Send data to device
    def send(self, message, wait_for_response=False):
        asyncio.run_coroutine_threadsafe(self.add_to_send_queue(message), self.event_loop)

        # Optionally block until a response is received
        if wait_for_response:
            return self.wait_for_response()
        return True

    def wait_for_response(self):
        # TODO: This is a potential race condition. If the device responds before this function is called,
        #   the flag with be cleared prematurely and will block until the next response or timeout. This
        #   is unlikely to happen but should be noted.
        self.response_available.clear()
        if not self.response_available.wait(self.config.response_timeout):
            self.logger.warning("Response timeout")
            return False
        self.response_available.clear()
        return True
