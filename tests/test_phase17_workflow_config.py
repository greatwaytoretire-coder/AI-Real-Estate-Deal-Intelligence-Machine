import unittest

from ai_real_estate_deal_intelligence_machine.phase17 import (
    RuleAction,
    RuleCondition,
    WorkflowRule,
    WorkflowConfigurationEngine,
)


class Phase17WorkflowConfigurationTests(unittest.TestCase):
    def test_rule_conditions_and_actions_are_created(self):
        condition = RuleCondition(
            field="Opportunity Score",
            operator=">=",
            value=85,
        )
        action = RuleAction(
            name="Create underwriting",
            sequence=1,
        )

        self.assertEqual(condition.field, "Opportunity Score")
        self.assertEqual(action.name, "Create underwriting")

    def test_workflow_rule_and_engine_build_configuration(self):
        engine = WorkflowConfigurationEngine()
        rule = engine.create_rule()
        action_plan = engine.create_actions(rule)

        self.assertIsInstance(rule, WorkflowRule)
        self.assertTrue(action_plan)
        self.assertEqual(rule.trigger, "Opportunity Score >= 85")


if __name__ == "__main__":
    unittest.main()
