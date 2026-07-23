import unittest
from pathlib import Path
from unittest.mock import MagicMock

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase30 import ContinuousRuntime, OperatingMode
from ai_real_estate_deal_intelligence_machine.jobs.base import JobStatus
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase29 import (
    MarketConfig,
    ScalingManager,
)


class Phase30ProductionRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase30_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)

        # Mock the high-level dependencies required by the modern ContinuousRuntime
        self.provider_manager = MagicMock(spec=ProviderManager)
        self.orchestrator = MagicMock()
        self.scaling_manager = ScalingManager()

        # Configure a test market
        self.scaling_manager.load_market_config(
            MarketConfig(market_id="test_market", market_name="Test Market", data_providers=["mock_provider_a"])
        )

        self.runtime = ContinuousRuntime(self.audit_logger, self.provider_manager, self.orchestrator, self.scaling_manager)

    def tearDown(self):
        self.log_path.unlink(missing_ok=True)

    def test_continuous_runtime_flow(self):
        """
        PHASE 30: Verify the end-to-end continuous runtime flow.
        """
        self.runtime.mode = OperatingMode.MOCK

        # Mock the provider's response
        mock_provider = MagicMock()
        self.provider_manager.providers = {"mock_provider_a": mock_provider}

        # 1. Ingest new data from a provider
        mock_provider.fetch.return_value = [
            {"id": "rec-001", "provider": "mock_provider_a", "address": "123 Main St", "zip": "12345"},
            {"id": "rec-002", "provider": "mock_provider_a", "address": "456 Oak Ave", "zip": "67890"},
        ]
        ingestion_run = self.runtime.run_ingestion_for_market("test_market", {})

        self.assertEqual(ingestion_run.records_discovered, 2)
        self.assertEqual(ingestion_run.records_inserted, 2)
        self.assertEqual(ingestion_run.records_skipped, 0)
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 2)

        # Mock the orchestrator's behavior for the worker
        self.orchestrator.handle_job.return_value = MagicMock(error=None)

        # 2. Ingest duplicate data and verify deduplication
        mock_provider.fetch.return_value = [
            {"id": "rec-003", "provider": "mock_provider_a", "address": "123 Main St", "zip": "12345"},
        ]
        ingestion_run_2 = self.runtime.run_ingestion_for_market("test_market", {})
        self.assertEqual(ingestion_run_2.records_discovered, 1)
        self.assertEqual(ingestion_run_2.records_inserted, 0)
        self.assertEqual(ingestion_run_2.records_skipped, 1)
        # No new job should be created
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 2)

        # 3. Have a worker process a job successfully
        self.runtime.worker.run()
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 1)
        # Find the completed job
        completed_job = next(j for j in self.runtime.job_queue.jobs.values() if j.status == JobStatus.COMPLETED)
        self.assertIsNotNone(completed_job)

        # 4. Have a worker process a job that fails
        # The next job in the queue will be for "456 Oak Ave"
        failing_job_id = self.runtime.job_queue.pending_queue[0]
        self.runtime.worker.run(failure_simulation=True)

        # Verify it was moved to the dead-letter queue
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 0)
        self.assertEqual(len(self.runtime.job_queue.dead_letter_queue), 1)
        failed_job = self.runtime.job_queue.dead_letter_queue[0]
        self.assertEqual(failed_job.job_id, failing_job_id)
        self.assertEqual(failed_job.status, JobStatus.FAILED)

        # 5. Verify audit logs were created
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn("INGESTION_RUN_COMPLETED", log_contents)
            self.assertIn("WORKER_START", log_contents)
            self.assertIn("AI_PIPELINE_SUCCESS", log_contents)
            self.assertIn("WORKER_ERROR", log_contents)