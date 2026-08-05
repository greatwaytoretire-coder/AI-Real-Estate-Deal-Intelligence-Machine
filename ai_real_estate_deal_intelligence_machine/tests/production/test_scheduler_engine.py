from ai_real_estate_deal_intelligence_machine.production.scheduler_engine import (
    SchedulerEngine,
)

from ai_real_estate_deal_intelligence_machine.production.scheduler_models import (
    JobStatus,
)


def test_scheduler_tracks_completed_jobs():

    engine = SchedulerEngine()

    engine.schedule_job(
        "Nightly Market Scan",
        JobStatus.COMPLETED,
    )

    report = engine.generate_report()

    assert report.total_jobs == 1
    assert report.completed_jobs == 1
    assert report.failed_jobs == 0


def test_scheduler_tracks_failed_jobs():

    engine = SchedulerEngine()

    engine.schedule_job(
        "MLS Sync",
        JobStatus.FAILED,
    )

    report = engine.generate_report()

    assert report.total_jobs == 1
    assert report.failed_jobs == 1