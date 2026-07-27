import sqlite3
import unittest
from pathlib import Path
from datetime import datetime, timedelta

from .db_client import DatabaseClient
from .jobs.base import Job, JobStatus
from .persistent_job_queue import PersistentJobQueue


class PersistentJobQueueTest(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for each test."""
        self.db_path = Path("data/test_persistent_queue.db")
        self.db_path.unlink(missing_ok=True)
        self.db_client = DatabaseClient(database_path=self.db_path)
        self.queue = PersistentJobQueue(db_client=self.db_client)

    def tearDown(self):
        """Clean up the temporary database after each test."""
        self.db_client.close()
        self.db_path.unlink(missing_ok=True)

    def test_submit_and_retrieve_job(self):
        """Verify a job can be submitted, is pending, and can be retrieved."""
        job = Job(job_id="job-001", payload={"data": "test"})

        # 1. Submit the job
        self.assertTrue(self.queue.submit_job(job))

        # 2. Verify the queue is now "truthy"
        self.assertTrue(self.queue.pending_queue)

        # 3. Retrieve the job
        retrieved_job = self.queue.get_pending_job()
        self.assertIsNotNone(retrieved_job)
        self.assertEqual(retrieved_job.job_id, "job-001")

        # 4. Verify its status was updated to RUNNING in the database
        db_job = self.db_client.get_job("job-001")
        self.assertEqual(db_job.status, JobStatus.RUNNING)

        # 5. Verify the queue is now empty
        self.assertFalse(self.queue.pending_queue)

    def test_get_pending_job_returns_none_when_empty(self):
        """Verify get_pending_job returns None when the queue is empty."""
        self.assertFalse(self.queue.pending_queue)
        self.assertIsNone(self.queue.get_pending_job())

    def test_job_order_is_fifo(self):
        """Verify jobs are processed in First-In, First-Out order."""
        job1 = Job(job_id="job-001", payload={})
        job2 = Job(job_id="job-002", payload={})

        self.queue.submit_job(job1)
        # Simulate a small delay to ensure created_at is different
        import time
        time.sleep(0.01)
        self.queue.submit_job(job2)

        # First job retrieved should be job1
        first_job = self.queue.get_pending_job()
        self.assertEqual(first_job.job_id, "job-001")

        # Second job retrieved should be job2
        second_job = self.queue.get_pending_job()
        self.assertEqual(second_job.job_id, "job-002")

    def test_retry_and_dead_letter_lifecycle(self):
        """Verify the retry and DLQ mechanisms work correctly."""
        job = Job(job_id="job-retry", payload={}, attempts=1)
        self.queue.submit_job(job)

        # 1. Simulate a worker scheduling a retry
        # The worker now calls the public `schedule_for_retry` method.
        job.attempts = 1 # Worker would have incremented this.
        self.queue.schedule_for_retry(job)

        # Verify the job status is now RETRY_SCHEDULED in the DB
        db_job_retry = self.db_client.get_job("job-retry")
        self.assertEqual(db_job_retry.status, JobStatus.RETRY_SCHEDULED)
        self.assertEqual(db_job_retry.attempts, 1)
        self.assertTrue(self.queue.pending_queue)

        # 2. Retrieve the retry-scheduled job
        retrieved_job = self.queue.get_pending_job()
        self.assertEqual(retrieved_job.job_id, "job-retry")
        self.assertEqual(retrieved_job.status, JobStatus.RUNNING)

        # 3. Simulate the job failing permanently and moving to DLQ
        self.db_client.update_job_status("job-retry", JobStatus.DEAD_LETTER)

        # Verify the pending queue is empty and the DLQ has one item
        self.assertFalse(self.queue.pending_queue)
        dlq = self.queue.dead_letter_queue
        self.assertEqual(len(dlq), 1)
        self.assertEqual(dlq[0].job_id, "job-retry")

    def test_submit_job_propagates_db_errors(self):
        """Verify that database errors are not silently swallowed."""
        job = Job(job_id="job-001", payload={})
        self.queue.submit_job(job)

        # Submitting the same job ID again should raise an IntegrityError
        # because of the PRIMARY KEY constraint.
        with self.assertRaises(sqlite3.IntegrityError):
            self.queue.submit_job(job)

    def test_job_persists_across_restarts(self):
        """
        Verify that a submitted job survives a simulated process restart.
        """
        job_to_persist = Job(
            job_id="job-persistent-001",
            payload={"data": "survives_restart"},
            status=JobStatus.PENDING,
            attempts=0,
        )

        # 1. Submit a job to the first queue instance
        self.queue.submit_job(job_to_persist)

        # 2. Simulate a restart by closing the DB connection and creating new instances
        self.db_client.close()

        with DatabaseClient(database_path=self.db_path) as new_db_client:
            new_queue = PersistentJobQueue(db_client=new_db_client)

            # 3. Verify the job is available in the new queue instance
            retrieved_job = new_queue.get_pending_job()
            self.assertIsNotNone(retrieved_job)
            self.assertEqual(retrieved_job.job_id, job_to_persist.job_id)
            self.assertEqual(retrieved_job.payload, job_to_persist.payload)
            self.assertEqual(retrieved_job.attempts, job_to_persist.attempts)


class PersistentJobRecoveryTest(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for each test."""
        self.db_path = Path("data/test_recovery.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.db_path.unlink(missing_ok=True)
        self.db_client = DatabaseClient(database_path=self.db_path)
        self.queue = PersistentJobQueue(db_client=self.db_client)
        self.stale_timeout = 300  # 5 minutes

    def tearDown(self):
        """Clean up the temporary database after each test."""
        self.db_client.close()
        self.db_path.unlink(missing_ok=True)

    def _create_and_run_job(self, job_id: str, attempts: int = 1) -> Job:
        """Helper to create a job and immediately set it to RUNNING."""
        job = Job(job_id=job_id, payload={"id": job_id}, attempts=attempts)
        self.queue.submit_job(job)
        running_job = self.queue.get_pending_job()
        self.assertEqual(running_job.status, JobStatus.RUNNING)
        return self.db_client.get_job(job_id)

    def _make_job_stale(self, job_id: str):
        """Helper to manually set a job's updated_at timestamp to be old."""
        stale_timestamp = (datetime.utcnow() - timedelta(seconds=self.stale_timeout + 60)).isoformat()
        with self.db_client._connection as conn:
            conn.execute("UPDATE jobs SET updated_at = ? WHERE job_id = ?", (stale_timestamp, job_id))

    def test_stale_running_job_is_recovered(self):
        """TEST 1: Stale RUNNING job is recovered to RETRY_SCHEDULED."""
        job = self._create_and_run_job("stale-job", attempts=2)
        self._make_job_stale(job.job_id)

        recovered_count = self.queue.recover_stale_jobs(self.stale_timeout)
        self.assertEqual(recovered_count, 1)

        recovered_job = self.db_client.get_job(job.job_id)
        self.assertEqual(recovered_job.status, JobStatus.RETRY_SCHEDULED)
        self.assertEqual(recovered_job.attempts, 2, "Attempts should be preserved")

    def test_fresh_running_job_is_not_recovered(self):
        """TEST 2: A recent RUNNING job is not touched."""
        job = self._create_and_run_job("fresh-job")

        recovered_count = self.queue.recover_stale_jobs(self.stale_timeout)
        self.assertEqual(recovered_count, 0)

        fresh_job = self.db_client.get_job(job.job_id)
        self.assertEqual(fresh_job.status, JobStatus.RUNNING)

    def test_jobs_in_terminal_or_pending_states_are_not_modified(self):
        """TEST 3-6: Jobs in other states are not affected by recovery."""
        # Create jobs in various states
        jobs_to_test = {
            JobStatus.COMPLETED: "completed-job",
            JobStatus.DEAD_LETTER: "dlq-job",
            JobStatus.PENDING: "pending-job",
            JobStatus.RETRY_SCHEDULED: "retry-job",
        }

        for status, job_id in jobs_to_test.items():
            job = Job(job_id=job_id, payload={})
            self.db_client.create_job(job)
            self.db_client.update_job_status(job_id, status)
            # Make them appear stale to confirm they are ignored regardless of timestamp
            self._make_job_stale(job_id)

        recovered_count = self.queue.recover_stale_jobs(self.stale_timeout)
        self.assertEqual(recovered_count, 0)

        for status, job_id in jobs_to_test.items():
            unaffected_job = self.db_client.get_job(job_id)
            self.assertEqual(unaffected_job.status, status)

    def test_recovery_survives_database_reopen(self):
        """TEST 7: Recovery state is durable across connections."""
        job = self._create_and_run_job("persistent-stale-job")
        self._make_job_stale(job.job_id)

        # Run recovery
        self.queue.recover_stale_jobs(self.stale_timeout)
        self.db_client.close()

        with DatabaseClient(database_path=self.db_path) as new_db_client:
            # Reopen the database and check the state
            reopened_job = new_db_client.get_job(job.job_id)
            self.assertEqual(reopened_job.status, JobStatus.RETRY_SCHEDULED)

    def test_production_startup_recovery_simulation(self):
        """
        TEST 8: Verify startup recovery logic from main.py works as expected.
        This test simulates the core logic of create_production_services.
        """
        # 1. Create a stale job directly in the database
        job = self._create_and_run_job("stale-at-startup")
        self._make_job_stale(job.job_id)
        self.db_client.close() # Simulate process shutdown

        with DatabaseClient(database_path=self.db_path) as db_client:
            # 2. Simulate the application startup sequence
            queue = PersistentJobQueue(db_client=db_client)

            # This is the line from main.py
            recovered_count = queue.recover_stale_jobs(stale_after_seconds=self.stale_timeout)

            # 3. Assertions
            self.assertEqual(recovered_count, 1)
            recovered_job = db_client.get_job(job.job_id)
            self.assertEqual(recovered_job.status, JobStatus.RETRY_SCHEDULED)