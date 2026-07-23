import os
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.config import DATA_DIR
from ai_real_estate_deal_intelligence_machine.phase24 import DataSourceType
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager


class Phase26DataProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.log_path = DATA_DIR / "test_phase26_audit.log"
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)

    def tearDown(self):
        self.log_path.unlink(missing_ok=True)
        if "ATTOM_API_KEY" in os.environ:
            del os.environ["ATTOM_API_KEY"]

    def test_provider_manager_fallback_and_live_mode(self):
        """
        PHASE 26: Verify provider manager falls back to mock when API key is missing,
        and uses live provider when it is present.
        """
        # 1. Test Fallback Behavior (API key is NOT set)
        if "ATTOM_API_KEY" in os.environ:
            del os.environ["ATTOM_API_KEY"]

        manager_mock_mode = ProviderManager(audit_logger=self.audit_logger)
        self.assertIn("attom", manager_mock_mode.providers)
        mock_provider = manager_mock_mode.providers["attom"]

        # Fetch data and verify it's from the MOCK source
        records_mock = mock_provider.fetch({"zip": "12345"})
        self.assertEqual(len(records_mock), 1)
        self.assertEqual(mock_provider.get_config().source_type, DataSourceType.MOCK)
        self.assertEqual(records_mock[0]['source'], "mock")

        # 2. Test Live Behavior (API key IS set)
        os.environ["ATTOM_API_KEY"] = "test-key-is-set"

        manager_live_mode = ProviderManager(audit_logger=self.audit_logger)
        live_provider = manager_live_mode.providers["attom"]

        # Fetch data and verify it's from the LIVE source
        records_live = live_provider.fetch({"zip": "54321"})
        self.assertEqual(len(records_live), 1)
        self.assertEqual(live_provider.get_config().source_type, DataSourceType.LIVE)
        self.assertEqual(records_live[0]['provider'], "attom_api")