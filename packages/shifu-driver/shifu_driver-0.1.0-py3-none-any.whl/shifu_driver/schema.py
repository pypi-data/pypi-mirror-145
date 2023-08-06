import dataclasses
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
import json


class ExpandedJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder class for handling serialization of additional object types"""

    # Override the default 'default' method to serialize other types
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.name

        # Call the base class to handle other type or raise TypeError
        return super().default(obj)


# Enum for all possible connection states
class ConnectionState(Enum):
    CONNECTED = auto()
    CONNECTION_IN_PROGRESS = auto()
    CONNECTION_FAILED = auto()
    WATCHDOG_FAILED = auto()
    DISCONNECTED = auto()


# Enum for all possible internal device states
class DeviceState(Enum):
    IDLE = auto()
    IN_USE = auto()
    EMERGENCY_STOPPED = auto()
    ERROR = auto()
    DISABLED = auto()


class JSONObject:
    def to_dict(self):
        return dataclasses.asdict(self)

    def __str__(self):
        return json.dumps(self, indent=4, cls=ExpandedJSONEncoder)


@dataclass
class DeviceStatus(JSONObject):
    # Data class storing info about the current internal state of a device
    state: DeviceState = DeviceState.IDLE
    error_info: str = ""


@dataclass
class ConnectionStatus(JSONObject):
    # Current connection state of device
    state: ConnectionState = ConnectionState.DISCONNECTED
    start_time: datetime = datetime.min
    requests_received: int = 0
    events_published: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    heartbeat_packets_sent: int = 0
    heartbeat_packets_received: int = 0
    heartbeat_failure_count: int = 0
    last_heartbeat_sent: datetime = datetime.min
    last_heartbeat_received: datetime = datetime.min


# Data class representing the configuration of a device
@dataclass
class Config(JSONObject):
    # Connection settings
    device_ip: str = '127.0.0.1'
    device_port: int = 1234
    backend_type: str = 'client'
    term_char: str = '\n'

    # Watchdog settings
    heartbeat_send_delay: float = 1.0  # Rate for sending heartbeat requests (in seconds)
    heartbeat_timeout: int = 2  # Time before device times out (in seconds)
    heartbeat_failure_limit: int = 3  # Number of times a device can time out before being marked dead
    heartbeat_logging: bool = False  # Sets whether to log heartbeat requests and responses

    @staticmethod
    def from_json(json):
        return Config(
            device_ip=json.get('device_ip', '127.0.0.1'),
            device_port=json.get('device_port', '1234'),
            backend_type=json.get('backend_type', 'client'),
            term_char=json.get('term_char', '\n'),
            heartbeat_send_delay=json.get('heartbeat_send_delay', 1.0),
            heartbeat_timeout=json.get('heartbeat_timeout', 2),
            heartbeat_failure_limit=json.get('heartbeat_failure_limit', 3),
            heartbeat_logging=json.get('heartbeat_logging', False),
        )
