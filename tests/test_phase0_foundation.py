import unittest

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.config import settings
from ai_real_estate_deal_intelligence_machine.db_client import DatabaseClient
from ai_real_estate_deal_intelligence_machine.provider_registry import ProviderRegistry


class Phase0FoundationTests(unittest.TestCase):
    def test_settings_use_zero_budget_local_defaults(self):
        self.assertEqual(settings.app_env, "development")
        self.assertTrue(settings.mock_provider_mode)
        self.assertEqual(settings.autonomy_mode, "supervised")

    def test_provider_registry_returns_only_mock_providers(self):
        registry = ProviderRegistry()
        providers = registry.enabled_providers()

        self.assertGreaterEqual(len(providers), 1)
        self.assertTrue(all(provider["source_type"] == "mock" for provider in providers))

    def test_database_client_can_initialize_and_store_audit_rows(self):
        client = DatabaseClient()
        try:
            client.upsert_provider("mock_property_feed", "Mock Property Feed", "mock")
            client.log_audit("NEW_PROPERTY_DISCOVERED", "Phase 0 provider bootstrap")
            audit_logs = client.list_audit_logs()
            self.assertGreaterEqual(len(audit_logs), 1)
        finally:
            client.close()

    def test_audit_logger_writes_traceable_log_entries(self):
        logger = AuditLogger()
        logger.log("PHASE0_BOOTSTRAP", "Foundation initialization")


if __name__ == "__main__":
    unittest.main()
