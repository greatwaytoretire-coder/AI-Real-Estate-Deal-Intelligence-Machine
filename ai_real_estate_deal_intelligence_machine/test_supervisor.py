import unittest
from unittest.mock import MagicMock, call

from .supervisor import SystemSupervisor


class SupervisorTest(unittest.TestCase):
    def setUp(self):
        self.mock_market_orchestrator = MagicMock()
        self.mock_runtime = MagicMock()
        self.mock_logger = MagicMock()

        self.supervisor = SystemSupervisor(
            multi_market_orchestrator=self.mock_market_orchestrator,
            runtime=self.mock_runtime,
            audit_logger=self.mock_logger,
        )

    def test_run_single_cycle_ingestion_and_processing(self):
        """Verify a single cycle runs ingestion and processes the job queue."""
        # Simulate a queue with two pending jobs
        self.mock_runtime.job_queue.pending_queue = ["job1", "job2"]

        # To make the while loop terminate, the worker's run method must empty the queue
        def process_one_job(*args, **kwargs):
            self.mock_runtime.job_queue.pending_queue.pop(0)

        self.mock_runtime.worker.run.side_effect = process_one_job

        self.supervisor.run_single_cycle()

        # Verify ingestion was called once
        self.mock_market_orchestrator.run_all_active_markets.assert_called_once_with({})

        # Verify the worker was called twice to clear the queue
        self.assertEqual(self.mock_runtime.worker.run.call_count, 2)

    def test_supervisor_handles_errors_gracefully(self):
        """Verify the supervisor logs an error but does not crash."""
        # Simulate an exception during ingestion
        self.mock_market_orchestrator.run_all_active_markets.side_effect = ValueError("Simulated ingestion error")

        # This test is for the continuous loop, so we need a way to stop it
        self.supervisor.stop()
        self.supervisor.run_continuously()

        # Verify that the error was logged
        self.mock_logger.log.assert_any_call("SUPERVISOR_ERROR", "An unhandled error occurred in the main loop: Simulated ingestion error")

    def test_stop_event_terminates_loop(self):
        """Verify the stop event gracefully terminates the processing loop."""
        # Simulate a job that never finishes to test if stop() breaks the loop
        self.mock_runtime.job_queue.pending_queue = ["job1"]
        self.supervisor.stop() # Signal stop immediately
        self.supervisor.run_single_cycle()
        # The worker should not have been called because the stop event was set
        self.mock_runtime.worker.run.assert_not_called()