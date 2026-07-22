import unittest

from ai_real_estate_deal_intelligence_machine.phase16 import (
    MachineStatus,
    MissionControlDashboard,
    MissionControlMetrics,
)


class Phase16MissionControlTests(unittest.TestCase):
    def test_machine_status_has_required_states(self):
        self.assertIn(MachineStatus.RUNNING, MachineStatus)
        self.assertIn(MachineStatus.PAUSED, MachineStatus)
        self.assertIn(MachineStatus.DEGRADED, MachineStatus)
        self.assertIn(MachineStatus.ERROR, MachineStatus)

    def test_mission_control_dashboard_builds_sections(self):
        dashboard = MissionControlDashboard()
        self.assertIn("MACHINE STATUS", dashboard.render())
        self.assertIn("TODAY'S MACHINE ACTIVITY", dashboard.render())
        self.assertIn("TOP OPPORTUNITIES", dashboard.render())
        self.assertIn("MACHINE ACTIVITY FEED", dashboard.render())
        self.assertIn("EXCEPTIONS", dashboard.render())
        self.assertIn("PERFORMANCE", dashboard.render())

    def test_metrics_track_core_counts(self):
        metrics = MissionControlMetrics()
        self.assertEqual(metrics.properties_analyzed, 0)
        self.assertEqual(metrics.markets_analyzed, 0)
        self.assertEqual(metrics.buyers_analyzed, 0)


if __name__ == "__main__":
    unittest.main()
