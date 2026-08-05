from datetime import datetime, timezone

from .production_models import (
    ServiceHealth,
    ServiceStatus,
    SystemHealthReport,
)


class HealthMonitor:
    """
    Production health monitoring foundation.

    Tracks system components and produces
    operational health reports.
    """

    def __init__(self):
        self.services = []

    def register_service(
        self,
        service_name: str,
        status: ServiceStatus = ServiceStatus.HEALTHY,
        message: str = "Service operational",
    ):
        health = ServiceHealth(
            service_name=service_name,
            status=status,
            message=message,
            checked_at=datetime.now(timezone.utc),
        )

        self.services.append(health)

        return health

    def generate_report(self):

        healthy = sum(
            1
            for service in self.services
            if service.status == ServiceStatus.HEALTHY
        )

        failed = sum(
            1
            for service in self.services
            if service.status == ServiceStatus.FAILED
        )

        if failed > 0:
            overall = ServiceStatus.FAILED
        elif healthy < len(self.services):
            overall = ServiceStatus.DEGRADED
        else:
            overall = ServiceStatus.HEALTHY

        return SystemHealthReport(
            overall_status=overall,
            services_checked=len(self.services),
            healthy_services=healthy,
            failed_services=failed,
            generated_at=datetime.now(timezone.utc),
        )