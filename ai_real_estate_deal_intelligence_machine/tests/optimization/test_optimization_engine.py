from datetime import datetime, timezone

from ai_real_estate_deal_intelligence_machine.feedback.feedback_models import (
    DealFeedback,
)
from ai_real_estate_deal_intelligence_machine.optimization.optimization_engine import (
    OptimizationEngine,
)


def test_optimization_engine_returns_recommendation():

    engine = OptimizationEngine()

    feedback = DealFeedback(
        deal_id="TEST-1",
        predicted_profit=50000,
        actual_profit=45000,
        accuracy_score=0.60,
        created_at=datetime.now(timezone.utc),
    )

    recommendations = engine.evaluate_feedback([feedback])

    assert len(recommendations) == 1

    assert recommendations[0].confidence > 0