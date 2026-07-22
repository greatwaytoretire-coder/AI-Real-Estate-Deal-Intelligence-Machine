import unittest

from ai_real_estate_deal_intelligence_machine.phase20 import (
    EmergencyStopControls,
    MachineHealthMonitor,
    ProductionDeploymentAgent,
)


class Phase20ProductionDeploymentTests(unittest.TestCase):
    def test_emergency_stop_controls_are_present(self):
        controls = EmergencyStopControls()
        self.assertTrue(controls.pause_all_agents)
        self.assertTrue(controls.pause_acquisition)
        self.assertTrue(controls.pause_disposition)
        self.assertTrue(controls.pause_specific_provider)
        self.assertTrue(controls.pause_specific_agent)
        self.assertTrue(controls.pause_all_outbound_communication)

    def test_production_deployment_agent_creates_monitor_and_report(self):
        agent = ProductionDeploymentAgent()
        monitor = agent.create_machine_health_monitor()
        report = agent.create_production_readiness_report(monitor)

        self.assertIsInstance(monitor, MachineHealthMonitor)
        self.assertTrue(report)


if __name__ == "__main__":
    unittest.main()
