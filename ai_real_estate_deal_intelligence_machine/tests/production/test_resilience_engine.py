from ai_real_estate_deal_intelligence_machine.production.resilience_engine import (
    ResilienceEngine,
)

from ai_real_estate_deal_intelligence_machine.production.resilience_models import (
    RecoveryStatus,
)


def test_resilience_tracks_recovery():

    engine = ResilienceEngine()

    engine.record_event(
        "workflow_engine",
        RecoveryStatus.RECOVERED,
        attempts=2,
    )

    report = engine.generate_report()

    assert report.total_events == 1
    assert report.recovered_events == 1
    assert report.failed_events == 0


def test_resilience_tracks_failure():

    engine = ResilienceEngine()

    engine.record_event(
        "database",
        RecoveryStatus.FAILED,
        attempts=3,
    )

    report = engine.generate_report()

    assert report.total_events == 1
    assert report.failed_events == 1