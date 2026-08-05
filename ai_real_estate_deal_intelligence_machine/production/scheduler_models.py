from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ScheduledJob:
    name: str
    status: JobStatus
    scheduled_at: datetime


@dataclass
class SchedulerReport:
    total_jobs: int
    completed_jobs: int
    failed_jobs: int
    generated_at: datetime