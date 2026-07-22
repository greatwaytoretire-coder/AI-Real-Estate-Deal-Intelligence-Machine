import unittest

from ai_real_estate_deal_intelligence_machine.phase7 import (
    DealUnderwritingAgent,
    UnderwritingEvent,
    UnderwritingResult,
)


class Phase7UnderwritingEngineTests(unittest.TestCase):
    def test_underwriting_result_has_required_metrics(self):
        result = UnderwritingResult(
            strategy="WHOLESALE",
            purchase_price=180000,
            arv=210000,
            repairs=12000,
            closing_costs=5000,
            holding_costs=2500,
            financing=20000,
            selling_costs=9000,
            desired_profit=12000,
            assignment_fee=8000,
            cash_flow=3000,
        )

        for key in [
            "maximum_offer",
            "offer_range",
            "estimated_profit",
            "roi",
            "cash_on_cash_return",
            "cap_rate",
            "assignment_spread",
        ]:
            self.assertIn(key, result.as_dict())

    def test_deal_underwriting_agent_can_generate_underwriting_events(self):
        agent = DealUnderwritingAgent()
        event = agent.generate_event()

        self.assertEqual(event.event_type, "UNDERWRITING_UPDATED")
        self.assertTrue(event.payload)


if __name__ == "__main__":
    unittest.main()
