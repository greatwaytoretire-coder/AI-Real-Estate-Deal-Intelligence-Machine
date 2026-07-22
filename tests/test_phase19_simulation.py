import unittest

from ai_real_estate_deal_intelligence_machine.phase19 import (
    EndToEndSimulationEngine,
    SimulationEvent,
    SimulationResult,
)


class Phase19SimulationTests(unittest.TestCase):
    def test_simulation_engine_generates_workflow_and_failure_scenarios(self):
        engine = EndToEndSimulationEngine()
        result = engine.run_simulation()

        self.assertIsInstance(result, SimulationResult)
        self.assertTrue(result.events)
        self.assertIn("NEW PROPERTY", result.stages)
        self.assertIn("BUYER RESPONSE", result.stages)
        self.assertTrue(result.failure_modes)

    def test_simulation_event_has_expected_trigger_and_agent(self):
        event = SimulationEvent(
            stage="DISCOVERY",
            agent="PropertyDiscoveryAgent",
            workflow="Property discovery workflow",
            trigger="new property",
            outcome="success",
        )

        self.assertEqual(event.stage, "DISCOVERY")
        self.assertEqual(event.agent, "PropertyDiscoveryAgent")
        self.assertEqual(event.workflow, "Property discovery workflow")


if __name__ == "__main__":
    unittest.main()
