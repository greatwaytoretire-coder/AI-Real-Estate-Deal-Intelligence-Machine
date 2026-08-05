from ai_real_estate_deal_intelligence_machine.production.health_monitor import (
    HealthMonitor,
)

from ai_real_estate_deal_intelligence_machine.production.production_models import (
    ServiceStatus,
)


def test_health_monitor_reports_system_status():

    monitor = HealthMonitor()

    monitor.register_service(
        "database",
        ServiceStatus.HEALTHY,
    )

    monitor.register_service(
        "ai_engine",
        ServiceStatus.HEALTHY,
    )

    report = monitor.generate_report()

    assert report.overall_status == ServiceStatus.HEALTHY
    assert report.services_checked == 2
    assert report.healthy_services == 2
    assert report.failed_services == 0


def test_health_monitor_detects_failure():

    monitor = HealthMonitor()

    monitor.register_service(
        "database",
        ServiceStatus.FAILED,
        "Connection unavailable",
    )

    report = monitor.generate_report()

    assert report.overall_status == ServiceStatus.FAILED
    assert report.failed_services == 1