import unittest

from ai_real_estate_deal_intelligence_machine.phase13 import (
    DealRoom,
    DealRoomAccess,
    DealRoomAgent,
    DealRoomMetrics,
)


class Phase13DealRoomTests(unittest.TestCase):
    def test_deal_room_includes_required_sections(self):
        room = DealRoom(
            deal_id="deal-001",
            property_summary="Investor-ready property summary",
            location="Austin, TX",
            property_details={"beds": 3, "baths": 2},
            comps=["comp-001"],
            arv=220000,
            repairs=15000,
            underwriting={"maximum_offer": 190000},
            profit_analysis={"roi": 17.5},
            risk_analysis={"risk_score": 72},
            buyer_demand={"buyers": 4},
            data_confidence=0.84,
            access=DealRoomAccess(level="secure", token="token-001"),
            metrics=DealRoomMetrics(views=0, buyer_interest=0, questions=0, offers=0),
        )

        self.assertEqual(room.property_summary, "Investor-ready property summary")
        self.assertEqual(room.location, "Austin, TX")
        self.assertEqual(room.data_confidence, 0.84)

    def test_deal_room_agent_generates_room_and_updates(self):
        agent = DealRoomAgent()
        room = agent.generate_deal_room()
        update = agent.create_update(room)

        self.assertIsInstance(room, DealRoom)
        self.assertIsInstance(update, DealRoom)
        self.assertGreaterEqual(room.metrics.views, 0)

    def test_deal_room_access_is_secure(self):
        access = DealRoomAccess(level="secure", token="token-001")
        self.assertEqual(access.level, "secure")
        self.assertTrue(access.token)


if __name__ == "__main__":
    unittest.main()
