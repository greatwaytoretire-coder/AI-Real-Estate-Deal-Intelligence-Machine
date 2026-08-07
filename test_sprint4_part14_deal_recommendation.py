from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.deal_recommendation_integration import (
    DealRecommendationIntegration,
)


print("=" * 70)
print("SPRINT 4 PART 14 INTEGRATION TEST")
print("DEAL RECOMMENDATION INTELLIGENCE")
print("=" * 70)


# ----------------------------------------------------------------------
# STEP 1 - Investment Opportunities
# ----------------------------------------------------------------------

deals = [
    {
        "deal_id": "DEAL-001",
        "ranking_score": 84.5,
        "priority_action": "ANALYZE_NEXT",
        "success_probability": 81.0,
        "market_confidence": 80.0,
        "risk_level": "LOW",
    },
    {
        "deal_id": "DEAL-002",
        "ranking_score": 59.0,
        "priority_action": "WATCH",
        "success_probability": 65.0,
        "market_confidence": 70.0,
        "risk_level": "MEDIUM",
    },
    {
        "deal_id": "DEAL-003",
        "ranking_score": 25.0,
        "priority_action": "IGNORE",
        "success_probability": 30.0,
        "market_confidence": 40.0,
        "risk_level": "HIGH",
    },
]


print()
print("STEP 1 - Loading Investment Opportunities")
pprint(deals)


# ----------------------------------------------------------------------
# STEP 2 - Recommendation Integration
# ----------------------------------------------------------------------

engine = DealRecommendationIntegration()

result = engine.evaluate(deals)


print()
print("STEP 2 - Running Deal Recommendation Intelligence")
pprint(result)


# ----------------------------------------------------------------------
# STEP 3 - Final Recommendations
# ----------------------------------------------------------------------

print()
print("STEP 3 - Final Investment Recommendations")

for recommendation in result["recommendations"]:
    print(
        recommendation["deal_id"],
        "| Recommendation:",
        recommendation["recommendation"],
        "| Recommendation Score:",
        recommendation["recommendation_score"],
        "| Confidence:",
        recommendation["confidence_level"],
        "| Confidence Score:",
        recommendation["confidence_score"],
    )


# ----------------------------------------------------------------------
# STEP 4 - Validation
# ----------------------------------------------------------------------

assert result["total_deals"] == 3

assert len(
    result["recommendations"]
) == 3

assert (
    result["top_recommendation"]["deal_id"]
    == "DEAL-001"
)

assert (
    result["top_recommendation"]["recommendation"]
    == "PURSUE"
)

assert (
    result["top_recommendation"]["risk_level"]
    == "LOW"
)

assert (
    result["top_recommendation"]["confidence_level"]
    in {
        "HIGH",
        "MEDIUM",
    }
)

assert (
    result["status"]
    == "DEAL_RECOMMENDATIONS_COMPLETE"
)


print()
print("STEP 4 - Validation")
print("Validation successful")


print()
print("=" * 70)
print("SPRINT 4 PART 14 INTEGRATION TEST COMPLETE")
print("=" * 70)