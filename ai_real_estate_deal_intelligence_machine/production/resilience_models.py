from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class RecoveryStatus(str, Enum):
    HEALTHY = "healthy"
    RETRYING = "retrying"
    RECOVERED = "recovered"
    FAILED = "failed"


@dataclass
class RecoveryEvent:
    component: str
    status: RecoveryStatus
    attempts: int
    timestamp: datetime


@dataclass
class ResilienceReport:
    total_events: int
    recovered_events: int
    failed_events: int
    generated_at: datetime