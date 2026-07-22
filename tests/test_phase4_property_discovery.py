import unittest

from ai_real_estate_deal_intelligence_machine.phase4 import (
    DealCandidate,
    PropertyDiscoveryAgent,
    PropertyEvent,
    PropertyProfile,
)


class Phase4PropertyDiscoveryTests(unittest.TestCase):
    def test_property_profile_can_be_created(self):
        profile = PropertyProfile(
            address="101 Mock Street",
            price=215000,
            property_type="single_family",
            bedrooms=3,
            bathrooms=2,
            square_footage=1450,
            year_built=2005,
            days_on_market=21,
        )

        self.assertEqual(profile.address, "101 Mock Street")
        self.assertGreaterEqual(profile.score, 0)

    def test_property_discovery_agent_creates_candidate_records(self):
        agent = PropertyDiscoveryAgent()
        candidates = agent.find_deal_candidates()

        self.assertGreaterEqual(len(candidates), 1)
        self.assertTrue(all(isinstance(candidate, DealCandidate) for candidate in candidates))

    def test_property_event_emission_has_required_event_type(self):
        event = PropertyEvent(event_type="NEW_PROPERTY_DISCOVERED", payload={"address": "101 Mock Street"})
        self.assertEqual(event.event_type, "NEW_PROPERTY_DISCOVERED")


if __name__ == "__main__":
    unittest.main()
