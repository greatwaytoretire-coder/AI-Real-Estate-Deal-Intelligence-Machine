import unittest

from ai_real_estate_deal_intelligence_machine.phase34 import (
    BuyerActivity,
    BuyerContactInfo,
    BuyerInvestmentCriteria,
    EnhancedBuyerProfile,
)


class Phase34BuyerProfileTest(unittest.TestCase):
    def test_create_enhanced_buyer_profile(self):
        """
        PHASE 34: Verify the creation of the EnhancedBuyerProfile model.
        """
        profile = EnhancedBuyerProfile(
            name="John Doe",
            data_source="user_provided",
            confidence_score=0.95,
            verification_status="VERIFIED",
            proof_of_funds_verified=True,
            criteria=BuyerInvestmentCriteria(
                markets=["Austin, TX"],
                geographic_preferences=["78704", "78702"],
                property_types=["Single Family", "Duplex"],
                price_range_min=200000,
                price_range_max=500000,
                investment_strategies=["Fix and Flip"],
                rehab_tolerance="moderate",
            ),
            activity=BuyerActivity(
                deals_closed_last_12m=5,
                offers_made_last_90d=10,
            ),
            contact_info=BuyerContactInfo(
                email="john.doe@example.com",
            ),
        )

        self.assertEqual(profile.name, "John Doe")
        self.assertEqual(profile.criteria.rehab_tolerance, "moderate")
        self.assertEqual(profile.contact_info.email, "john.doe@example.com")
        self.assertTrue(profile.proof_of_funds_verified)