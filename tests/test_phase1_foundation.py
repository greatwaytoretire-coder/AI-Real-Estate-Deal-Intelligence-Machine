import unittest

from ai_real_estate_deal_intelligence_machine.phase1 import (
    AgentTaskQueue,
    EventBus,
    FoundationApp,
    MachineStatus,
    SystemHealth,
)


class Phase1FoundationTests(unittest.TestCase):
    def test_machine_status_has_required_states(self):
        status_states = set(MachineStatus)
        self.assertTrue({"RUNNING", "PAUSED", "DEGRADED", "ERROR"}.issubset(status_states))

    def test_foundation_app_builds_dashboard_sections(self):
        app = FoundationApp()
        sections = app.dashboard_sections()

        for section in [
            "Mission Control",
            "Opportunities",
            "Markets",
            "Buyers",
            "Sellers",
            "Deals",
            "AI Agents",
            "Activity",
            "Settings",
        ]:
            self.assertIn(section, sections)

    def test_system_health_reports_safe_overall_status(self):
        health = SystemHealth()
        self.assertIn(health.overall_status(), {"healthy", "degraded", "error"})

    def test_event_bus_and_queue_foundations_are_available(self):
        bus = EventBus()
        queue = AgentTaskQueue()

        bus.publish("NEW_PROPERTY_DISCOVERED", {"value": 1})
        queue.enqueue("analyze_property", {"value": 1})

        self.assertEqual(len(bus.events), 1)
        self.assertEqual(queue.size(), 1)


if __name__ == "__main__":
    unittest.main()
