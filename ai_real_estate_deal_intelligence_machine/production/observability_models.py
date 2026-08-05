from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class EventType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class SystemEvent:
    event_type: EventType
    source: str
    message: str
    created_at: datetime


@dataclass
class ObservabilityReport:
    total_events: int
    error_events: int
    warning_events: int
    generated_at: datetime