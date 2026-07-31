import unittest
from unittest.mock import MagicMock

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
        """
        Verify a single cycle runs ingestion and processes the job queue.
        """

        self.mock_runtime.job_queue.pending_queue = [
            "job1",
            "job2",
        ]


        def process_one_job(*args, **kwargs):
            self.mock_runtime.job_queue.pending_queue.pop(0)


        self.mock_runtime.worker.run.side_effect = process_one_job


        self.supervisor.run_single_cycle()


        self.mock_market_orchestrator.run_all_active_markets.assert_called_once_with(
            {}
        )


        self.assertEqual(
            self.mock_runtime.worker.run.call_count,
            2,
        )


    def test_supervisor_handles_errors_gracefully(self):
        """
        Verify continuous mode catches errors and logs them.
        """

        self.mock_market_orchestrator.run_all_active_markets.side_effect = (
            ValueError("Simulated ingestion error")
        )


        original_run_single_cycle = (
            self.supervisor.run_single_cycle
        )


        def run_once_then_stop():

            try:
                original_run_single_cycle()

            finally:
                self.supervisor.stop()


        self.supervisor.run_single_cycle = run_once_then_stop


        self.supervisor.run_continuously()


        self.mock_logger.log.assert_any_call(
            "SUPERVISOR_ERROR",
            "Simulated ingestion error",
        )


        self.mock_logger.log.assert_any_call(
            "SUPERVISOR_ERROR",
            "An unhandled error occurred in the main loop: Simulated ingestion error",
        )


    def test_stop_event_terminates_loop(self):
        """
        Verify the stop event gracefully terminates processing.
        """

        self.mock_runtime.job_queue.pending_queue = [
            "job1"
        ]


        self.supervisor.stop()


        self.supervisor.run_single_cycle()


        self.mock_runtime.worker.run.assert_not_called()


if __name__ == "__main__":
    unittest.main()