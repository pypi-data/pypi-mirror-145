"""Device watchdog"""
import asyncio
import contextlib
from datetime import datetime
import logging

from shifu_driver.schema import ConnectionState


class Watchdog:
    def __init__(self, send_heartbeat, connection_status, watchdog_config, event_loop):
        self.logger = logging.getLogger(__name__)

        # Set user-defined heartbeat sending function
        self.send_heartbeat = send_heartbeat

        # Set device connection state, task list, config refs
        self.connection = connection_status
        self.config = watchdog_config
        self.watchdog_tasks = set()
        self.event_loop = event_loop

        # Set heartbeat sending rate
        self.send_delay = self.config.heartbeat_send_delay
        self.max_delay = 30  # Max sending delay, in seconds

        # Watchdog flags
        self.watchdog_active = False
        self.rate_limit_active = False

    def start(self):
        asyncio.run_coroutine_threadsafe(self._start(), self.event_loop)

    async def _start(self):
        self.watchdog_active = True
        self.device_alive_flag = asyncio.Event()
        self.logger.debug(f"{self.config.reference_name} watchdog starting...")

        # Create watchdog tasks
        watchdog_task = asyncio.create_task(self.run_watchdog(), name='run_watchdog')
        timeout_task = asyncio.create_task(self.check_timeout(), name='check_timeout')

        # Add watchdog tasks to set of device tasks
        self.watchdog_tasks.add(watchdog_task)
        self.watchdog_tasks.add(timeout_task)

    def stop(self):
        asyncio.run_coroutine_threadsafe(self._stop(), self.event_loop)

    async def _stop(self):
        self.watchdog_active = False
        self.connection.heartbeat_failure_count = 0

        for task in self.watchdog_tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

    async def run_watchdog(self):
        self.logger.debug(f"{self.config.reference_name} watchdog started")

        while self.watchdog_active:
            await asyncio.sleep(self.get_send_delay())
            self.connection.last_heartbeat_sent = datetime.now()
            self.connection.heartbeat_packets_sent += 1
            # Optionally log heartbeat sent
            if self.config.heartbeat_logging:
                self.logger.debug("Send Heartbeat called")
            # before_heartbeat = time.time()
            self.send_heartbeat(self.config.heartbeat_timeout)
            # after_heartbeat = time.time()

        self.logger.debug(f"{self.config.reference_name} watchdog exiting")

    async def check_timeout(self):
        while self.watchdog_active:
            await asyncio.sleep(self.config.heartbeat_timeout)

            # Check if device heartbeat has timed out
            if (
                self.connection.last_heartbeat_sent - self.connection.last_heartbeat_received
            ).total_seconds() > self.config.heartbeat_timeout:
                self.logger.warning(f"Heartbeat timeout on {self.config.reference_name}")
                self.connection.heartbeat_failure_count += 1

            # Check if device has exceeded heartbeat failure limit
            if self.connection.heartbeat_failure_count >= self.config.heartbeat_failure_limit:
                self.logger.error(f"Heartbeat failure on {self.config.reference_name}")
                self.rate_limit_active = True
                self.connection.state = ConnectionState.WATCHDOG_FAILED

                # Wait for device to reconnect before continuing to check timeout
                self.device_alive_flag.clear()
                await self.device_alive_flag.wait()
                self.logger.info(f"{self.config.reference_name} reconnected")

    def feed_watchdog(self):
        self.connection.last_heartbeat_received = datetime.now()
        self.connection.heartbeat_packets_received += 1
        self.connection.heartbeat_failure_count = 0
        self.rate_limit_active = False

        # Signal that device is alive
        if not self.device_alive_flag.is_set():
            asyncio.run_coroutine_threadsafe(self.set_device_alive_flag(), self.event_loop)

        # Optionally log heartbeat received
        if self.config.heartbeat_logging:
            self.logger.debug("Heartbeat received")

    def get_send_delay(self):
        if not self.rate_limit_active:
            self.send_delay = self.config.heartbeat_send_delay
        elif self.send_delay < self.max_delay:
            self.send_delay = min(self.send_delay * 2, self.max_delay)
        else:
            self.send_delay = self.max_delay
        return self.send_delay

    async def set_device_alive_flag(self):
        self.device_alive_flag.set()

        # Reset to valid connection state if in watchdog failed state
        if self.connection.state == ConnectionState.WATCHDOG_FAILED:
            self.connection.state = ConnectionState.CONNECTED
