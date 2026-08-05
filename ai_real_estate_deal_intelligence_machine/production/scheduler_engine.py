from datetime import datetime, timezone

from .scheduler_models import (
    JobStatus,
    ScheduledJob,
    SchedulerReport,
)


class SchedulerEngine:
    """
    Phase 104

    Production scheduling foundation.
    """

    def __init__(self):
        self.jobs = []

    def schedule_job(
        self,
        name: str,
        status: JobStatus = JobStatus.PENDING,
    ):

        job = ScheduledJob(
            name=name,
            status=status,
            scheduled_at=datetime.now(timezone.utc),
        )

        self.jobs.append(job)

        return job

    def generate_report(self):

        completed = sum(
            1
            for job in self.jobs
            if job.status == JobStatus.COMPLETED
        )

        failed = sum(
            1
            for job in self.jobs
            if job.status == JobStatus.FAILED
        )

        return SchedulerReport(
            total_jobs=len(self.jobs),
            completed_jobs=completed,
            failed_jobs=failed,
            generated_at=datetime.now(timezone.utc),
        )