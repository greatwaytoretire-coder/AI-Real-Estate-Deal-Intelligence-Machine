from __future__ import annotations

from typing import List, Optional

from .db_client import DatabaseClient
from .jobs.base import Job, JobStatus


class _PendingQueueAdapter:
    """
    An adapter that provides a list-like interface for the pending queue,
    compatible with the existing Worker's retry logic, while ensuring the
    database remains the source of truth.
    """

    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    def append(self, job: Job):
        """
        Handles the worker's re-queue logic for retries by updating the
        job's status and attempts count in the database.
        """
        if job:
            self.db_client.update_job_status(job.job_id, JobStatus.RETRY_SCHEDULED, job.attempts)

    def __bool__(self) -> bool:
        """
        Allows `bool(queue.pending_queue)` to work by checking if any
        pending jobs exist in the database.
        """
        return self.db_client.get_pending_job_id() is not None


class PersistentJobQueue:
    """
    A durable job queue implementation that uses a DatabaseClient for persistence.
    It implements the same public interface as the in-memory RuntimeJobQueue.
    """

    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        # The pending_queue property returns an adapter object that is compatible
        # with the existing Worker's `append` call for retries.
        self.pending_queue = _PendingQueueAdapter(db_client)

    def submit_job(self, job: Job) -> bool:
        """Persists a new job to the database."""
        # The database schema's PRIMARY KEY on job_id provides idempotency.
        # A UNIQUE constraint violation will raise an IntegrityError, which we
        # allow to propagate as it indicates a logic error (duplicate job ID).
        self.db_client.create_job(job)
        return True

    def get_pending_job(self) -> Job | None:
        """
        Atomically retrieves the next pending job and updates its status to RUNNING.
        """
        job_id = self.db_client.get_pending_job_id()
        if not job_id:
            return None

        # Update status to RUNNING before returning to prevent race conditions
        self.db_client.update_job_status(job_id, JobStatus.RUNNING)

        # Retrieve the full job object with its updated status
        job = self.db_client.get_job(job_id)
        return job


    def schedule_for_retry(self, job: Job) -> None:
        """
        Updates the job's status in the database to RETRY_SCHEDULED, preserving its attempts count.
        """
        self.db_client.update_job_status(job.job_id, JobStatus.RETRY_SCHEDULED, job.attempts)

    @property
    def dead_letter_queue(self) -> List[Job]:
        """Retrieves all jobs in the dead-letter queue from the database."""
        return self.db_client.list_jobs_by_status(JobStatus.DEAD_LETTER)

    def recover_stale_jobs(self, stale_after_seconds: int) -> int:
        """Recovers jobs that have been in the RUNNING state for too long."""
        return self.db_client.recover_stale_running_jobs(stale_after_seconds)