import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase29 import (
    MarketConfig,
    MarketStatus,
    ScalingManager,
)
from ai_real_estate_deal_intelligence_machine.phase30 import (
    ContinuousRuntime,
    DeduplicationEngine,
    OperatingMode,
)


class Phase31LiveDataIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.log_path = Path(
            "data/test_phase31_audit.log"
        )

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_path.unlink(
            missing_ok=True
        )

        self.audit_logger = AuditLogger(
            log_path=self.log_path
        )

        os.environ.pop(
            "ATTOM_API_KEY",
            None,
        )

        self.provider_manager = ProviderManager(
            audit_logger=self.audit_logger
        )

        self.orchestrator = MagicMock()

        self.scaling_manager = ScalingManager()

    def tearDown(self):
        os.environ.pop(
            "ATTOM_API_KEY",
            None,
        )

        self.log_path.unlink(
            missing_ok=True
        )

    def create_runtime(self):
        return ContinuousRuntime(
            audit_logger=self.audit_logger,
            provider_manager=self.provider_manager,
            orchestrator=self.orchestrator,
            scaling_manager=self.scaling_manager,
            job_queue=None,
            deduplication_engine=DeduplicationEngine(),
        )

    def load_test_market(self):
        market_config = MarketConfig(
            market_id="test_market",
            market_name="Test Market",
            status=MarketStatus.ACTIVE,
            data_providers=["attom"],
        )

        self.scaling_manager.load_market_config(
            market_config
        )

    def test_end_to_end_ingestion_with_mock_fallback(self):
        runtime = self.create_runtime()

        runtime.mode = OperatingMode.PILOT

        self.load_test_market()

        ingestion_run = runtime.run_ingestion_for_market(
            "test_market",
            {"zip": "12345"},
        )

        self.assertEqual(
            ingestion_run.records_inserted,
            1,
        )

        self.assertEqual(
            len(runtime.job_queue.pending_queue),
            1,
        )

    def test_end_to_end_ingestion_with_live_provider(self):
        os.environ["ATTOM_API_KEY"] = (
            "test-key-is-set"
        )

        runtime = self.create_runtime()

        runtime.mode = OperatingMode.PILOT

        self.load_test_market()

        ingestion_run = runtime.run_ingestion_for_market(
            "test_market",
            {"zip": "54321"},
        )

        self.assertEqual(
            ingestion_run.records_inserted,
            1,
        )

        self.assertEqual(
            len(runtime.job_queue.pending_queue),
            1,
        )

    def test_live_provider_is_blocked_in_mock_mode(self):
        os.environ["ATTOM_API_KEY"] = (
            "test-key-is-set"
        )

        runtime = self.create_runtime()

        runtime.mode = OperatingMode.MOCK

        self.load_test_market()

        ingestion_run = runtime.run_ingestion_for_market(
            "test_market",
            {"zip": "54321"},
        )

        self.assertEqual(
            ingestion_run.records_inserted,
            0,
        )

        self.assertEqual(
            len(runtime.job_queue.pending_queue),
            0,
        )


if __name__ == "__main__":
    unittest.main()