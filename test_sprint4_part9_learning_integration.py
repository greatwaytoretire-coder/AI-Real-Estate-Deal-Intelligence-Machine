from ai_real_estate_deal_intelligence_machine.learning.pattern_memory import (
    PatternMemory,
)

from ai_real_estate_deal_intelligence_machine.learning.strategy_optimizer import (
    StrategyOptimizer,
)

from ai_real_estate_deal_intelligence_machine.learning.confidence_adjuster import (
    ConfidenceAdjuster,
)

from ai_real_estate_deal_intelligence_machine.learning.learning_feedback import (
    LearningFeedback,
)


print("=" * 70)
print("SPRINT 4 PART 9 INTEGRATION TEST")
print("LEARNING INTELLIGENCE INTEGRATION")
print("=" * 70)


print("\nSTEP 1 - Pattern Memory")

pattern_memory = PatternMemory()

pattern_memory.store(
    {
        "market": "Detroit",
        "property_type": "single_family",
        "success_rate": 85,
        "average_profit": 72000,
    }
)

patterns = pattern_memory.get_all()

print(patterns)


print("\nSTEP 2 - Strategy Optimization")

optimizer = StrategyOptimizer()

strategy_result = optimizer.optimize(
    confidence_data={
        "confidence_score": 60
    },
    detected_patterns=patterns,
)

print(strategy_result)


print("\nSTEP 3 - Confidence Adjustment")

adjuster = ConfidenceAdjuster()

confidence_result = adjuster.adjust(
    current_confidence=60,
    strategy_result=strategy_result,
)

print(confidence_result)


print("\nSTEP 4 - Learning Feedback")

feedback = LearningFeedback()

feedback_result = feedback.apply(
    deal_id="DEAL-001",
    confidence_result=confidence_result,
    strategy_result=strategy_result,
)

print(feedback_result)


print()
print("=" * 70)
print("SPRINT 4 PART 9 INTEGRATION TEST COMPLETE")
print("=" * 70)