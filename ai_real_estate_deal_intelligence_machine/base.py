from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class JobStatus(str, Enum):
    """Lifecycle of a job in the runtime queue."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    DEAD_LETTER = "DEAD_LETTER"


@dataclass
class Job:
    """A durable, trackable unit of work for the system."""

    # Fields from original ReliabilityJob
    job_id: str
    payload: Dict[str, Any]
    attempts: int = 0
    # Field for extended status tracking
    status: JobStatus = JobStatus.PENDING