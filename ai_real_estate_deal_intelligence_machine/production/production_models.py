from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass
class ServiceHealth:
    service_name: str
    status: ServiceStatus
    message: str
    checked_at: datetime


@dataclass
class SystemHealthReport:
    overall_status: ServiceStatus
    services_checked: int
    healthy_services: int
    failed_services: int
    generated_at: datetime
