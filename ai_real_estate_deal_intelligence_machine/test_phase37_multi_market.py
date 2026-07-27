import unittest
from pathlib import Path
from unittest.mock import MagicMock

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase29 import MarketConfig, MarketStatus, ScalingManager
from ai_real_estate_deal_intelligence_machine.phase30 import ContinuousRuntime, OperatingMode
from ai_real_estate_deal_intelligence_machine.phase36 import AgentOrchestrator
from ai_real_estate_deal_intelligence_machine.phase37 import MultiMarketOrchestrator


class Phase37MultiMarketTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase37_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)

        # Initialize all components needed for the runtime
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

        # For testing MultiMarketOrchestrator, we only need a component that satisfies the IngestionRunner protocol.
        # We can use a mock instead of a full ContinuousRuntime.
        self.mock_runtime = MagicMock()

    def test_multi_market_orchestrator_runs_active_markets(self):
        """PHASE 37: Verify the orchestrator runs ingestion only for active markets."""
        orchestrator = MultiMarketOrchestrator(self.scaling_manager, self.mock_runtime)

        # Run the orchestrator
        report = orchestrator.run_all_active_markets({})

        # Verify the report
        self.assertIn("atx", report.markets_processed)
        self.assertNotIn("dfw", report.markets_processed) # Should not be processed because it's PAUSED

        # Verify that run_ingestion_for_market was called once for the active market
        self.mock_runtime.run_ingestion_for_market.assert_called_once_with("atx", {})