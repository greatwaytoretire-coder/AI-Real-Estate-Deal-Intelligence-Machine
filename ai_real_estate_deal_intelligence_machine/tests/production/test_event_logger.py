from ai_real_estate_deal_intelligence_machine.production.event_logger import (
    EventLogger,
)

from ai_real_estate_deal_intelligence_machine.production.observability_models import (
    EventType,
)


def test_event_logger_records_events():

    logger = EventLogger()

    logger.record_event(
        "deal_engine",
        "Deal analysis completed",
        EventType.SUCCESS,
    )

    logger.record_event(
        "workflow_engine",
        "Workflow started",
        EventType.INFO,
    )

    report = logger.generate_report()

    assert report.total_events == 2
    assert report.error_events == 0
    assert report.warning_events == 0


def test_event_logger_tracks_errors():

    logger = EventLogger()

    logger.record_event(
        "database",
        "Database connection failed",
        EventType.ERROR,
    )

    report = logger.generate_report()

    assert report.total_events == 1
    assert report.error_events == 1