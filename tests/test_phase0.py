import unittest

from ai_real_estate_deal_intelligence_machine.phase0 import MissionControlDashboard, MockProviderRegistry


class Phase0MissionControlTests(unittest.TestCase):
    def test_dashboard_has_core_mission_control_metrics(self):
        dashboard = MissionControlDashboard()
        summary = dashboard.summary()

        self.assertEqual(summary["machine_status"], "ONLINE")
        self.assertGreaterEqual(summary["markets_monitored"], 1)
        self.assertGreaterEqual(summary["new_properties_discovered"], 1)
        self.assertGreaterEqual(summary["active_deal_pipelines"], 1)
        self.assertGreaterEqual(summary["high_priority_opportunities"], 1)

    def test_mock_provider_registry_tracks_only_mock_integrations(self):
        registry = MockProviderRegistry()
        providers = registry.enabled_providers()

        self.assertGreaterEqual(len(providers), 1)
        self.assertTrue(all(provider["source_type"] == "mock" for provider in providers))
        self.assertTrue(all("mock" in provider["label"].lower() for provider in providers))


if __name__ == "__main__":
    unittest.main()
