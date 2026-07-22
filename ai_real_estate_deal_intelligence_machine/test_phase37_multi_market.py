import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase29 import MarketConfig, MarketStatus, ScalingManager
from ai_real_estate_deal_intelligence_machine.phase30 import ContinuousRuntime, OperatingMode
from ai_real_estate_deal_intelligence_machine.phase36 import AgentOrchestrator


class Phase37MultiMarketTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase37_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)

        # Initialize all components needed for the runtime
        self.provider_manager = ProviderManager(audit_logger=self.audit_logger)
        self.orchestrator = AgentOrchestrator(audit_logger=self.audit_logger)
        self.scaling_manager = ScalingManager()

        # Configure two markets
        self.scaling_manager.load_market_config(
            MarketConfig(
                market_id="atx",
                market_name="Austin, TX",
                status=MarketStatus.ACTIVE,
                data_providers=["attom"], # Only uses the 'attom' provider (which will be mocked)
            )
        )
        self.scaling_manager.load_market_config(
            MarketConfig(
                market_id="dfw",
                market_name="Dallas, TX",
                status=MarketStatus.PAUSED, # This market is not active
                data_providers=["attom"],
            )
        )

        self.runtime = ContinuousRuntime(self.audit_logger, self.provider_manager, self.orchestrator, self.scaling_manager)
        self.runtime.mode = OperatingMode.PILOT

    def test_ingestion_respects_market_configuration(self):
        """PHASE 37: Verify ingestion runs only for active markets and their specified providers."""
        # Run ingestion for the active market (Austin)
        run_log_atx = self.runtime.run_ingestion_for_market("atx", {"query": "test"})
        self.assertEqual(run_log_atx.records_inserted, 1)
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 1)

        # Attempt to run ingestion for the paused market (Dallas)
        run_log_dfw = self.runtime.run_ingestion_for_market("dfw", {"query": "test"})
        self.assertEqual(run_log_dfw.records_inserted, 0)
        self.assertIn("is not active or does not exist", run_log_dfw.errors[0])
        self.assertEqual(len(self.runtime.job_queue.pending_queue), 1) # No new job created