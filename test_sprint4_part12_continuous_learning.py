from datetime import datetime, timezone

from ai_real_estate_deal_intelligence_machine.learning.prediction_memory import (
    PredictionMemory,
)

from ai_real_estate_deal_intelligence_machine.learning.continuous_learning_engine import (
    ContinuousLearningEngine,
)


print("=" * 70)
print("SPRINT 4 PART 12 INTEGRATION TEST")
print("CONTINUOUS INTELLIGENCE OPTIMIZATION")
print("=" * 70)


# ---------------------------------------------------------
# STEP 1 - Store Predictions
# ---------------------------------------------------------

print("\nSTEP 1 - Prediction Memory")


memory = PredictionMemory()


predictions = [
    {
        "deal_id": "DEAL-001",
        "predicted_outcome": "PROCEED",
        "success_probability": 81,
    },
    {
        "deal_id": "DEAL-002",
        "predicted_outcome": "PROCEED",
        "success_probability": 75,
    },
    {
        "deal_id": "DEAL-003",
        "predicted_outcome": "PASS",
        "success_probability": 30,
    },
]


for prediction in predictions:
    memory.store(prediction)


print(memory.get_all())


# ---------------------------------------------------------
# STEP 2 - Actual Deal Outcomes
# ---------------------------------------------------------

print("\nSTEP 2 - Closed Deal Outcomes")


outcomes = [
    {
        "deal_id": "DEAL-001",
        "actual_outcome": "PROCEED",
    },
    {
        "deal_id": "DEAL-002",
        "actual_outcome": "PASS",
    },
    {
        "deal_id": "DEAL-003",
        "actual_outcome": "PASS",
    },
]


print(outcomes)


# ---------------------------------------------------------
# STEP 3 - Continuous Learning
# ---------------------------------------------------------

print("\nSTEP 3 - Running Continuous Learning Engine")


engine = ContinuousLearningEngine()


result = engine.analyze(
    predictions=memory.get_all(),
    outcomes=outcomes,
)


print(result)


# ---------------------------------------------------------
# STEP 4 - Validation
# ---------------------------------------------------------

print("\nSTEP 4 - Validation")

assert (
    result["status"]
    ==
    "CONTINUOUS_LEARNING_COMPLETE"
)

assert (
    result["accuracy_analysis"]["accuracy"]
    ==
    66.67
)

assert (
    result["optimization"]["confidence_adjustment"]
    ==
    5
)


print("Validation successful")


print()
print("=" * 70)
print("SPRINT 4 PART 12 INTEGRATION TEST COMPLETE")
print("=" * 70)