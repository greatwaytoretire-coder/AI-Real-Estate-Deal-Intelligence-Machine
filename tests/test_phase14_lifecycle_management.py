import unittest

from ai_real_estate_deal_intelligence_machine.phase14 import (
    DealLifecycleStage,
    DealLifecycleWorkflow,
    NextBestActionEngine,
)


class Phase14LifecycleManagementTests(unittest.TestCase):
    def test_lifecycle_stage_enum_contains_required_stages(self):
        self.assertIn(DealLifecycleStage.DISCOVERED, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.ANALYZING, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.QUALIFIED, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.SELLER_ENGAGED, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.UNDERWRITING, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.OFFER, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.NEGOTIATION, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.UNDER_CONTRACT, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.DUE_DILIGENCE, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.DEAL_ROOM, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.BUYER_INTEREST, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.OFFERS, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.DISPOSITION, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.CLOSED, DealLifecycleStage)
        self.assertIn(DealLifecycleStage.OUTCOME_RECORDED, DealLifecycleStage)

    def test_workflow_and_next_best_action_engine_run(self):
        workflow = DealLifecycleWorkflow()
        actions = NextBestActionEngine().recommend_next_actions(workflow)

        self.assertTrue(actions)
        self.assertIn("Next Best Action", actions[0]["title"])


if __name__ == "__main__":
    unittest.main()
