from ai_real_estate_deal_intelligence_machine.learning.deal_ranking_integration import (
    DealRankingIntegration,
)


print("=" * 70)
print("SPRINT 4 PART 13 INTEGRATION TEST")
print("AUTONOMOUS DEAL RANKING INTELLIGENCE")
print("=" * 70)


# ---------------------------------------------------------
# STEP 1 - Load Opportunities
# ---------------------------------------------------------

print("\nSTEP 1 - Loading Investment Opportunities")


deals = [
    {
        "deal_id": "DEAL-001",
        "deal_score": 90,
        "market_confidence": 80,
        "seller_motivation": 95,
        "buyer_demand": 90,
        "profit_margin": 60,
        "risk_level": "LOW",
    },

    {
        "deal_id": "DEAL-002",
        "deal_score": 75,
        "market_confidence": 70,
        "seller_motivation": 80,
        "buyer_demand": 65,
        "profit_margin": 45,
        "risk_level": "MEDIUM",
    },

    {
        "deal_id": "DEAL-003",
        "deal_score": 55,
        "market_confidence": 40,
        "seller_motivation": 50,
        "buyer_demand": 45,
        "profit_margin": 25,
        "risk_level": "HIGH",
    },
]


print(deals)


# ---------------------------------------------------------
# STEP 2 - Run Ranking Intelligence
# ---------------------------------------------------------

print("\nSTEP 2 - Running Deal Ranking")


engine = DealRankingIntegration()


result = engine.evaluate(
    deals
)


print(result)


# ---------------------------------------------------------
# STEP 3 - Priority Queue
# ---------------------------------------------------------

print("\nSTEP 3 - Acquisition Priority Queue")


priority = result[
    "priority_result"
]


print(
    priority
)


# ---------------------------------------------------------
# STEP 4 - Validation
# ---------------------------------------------------------

print("\nSTEP 4 - Validation")


assert (
    result["status"]
    ==
    "DEAL_RANKING_INTEGRATION_COMPLETE"
)


assert (
    priority["status"]
    ==
    "PRIORITY_QUEUE_CREATED"
)


assert (
    priority["highest_priority"]["deal_id"]
    ==
    "DEAL-001"
)


print("Validation successful")


print()
print("=" * 70)
print("SPRINT 4 PART 13 INTEGRATION TEST COMPLETE")
print("=" * 70)