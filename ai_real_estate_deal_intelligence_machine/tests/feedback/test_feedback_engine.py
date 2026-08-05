from ai_real_estate_deal_intelligence_machine.feedback.feedback_engine import (
    FeedbackEngine,
)


def test_feedback_engine_calculates_accuracy():

    engine = FeedbackEngine()

    feedback = engine.evaluate_deal(
        deal_id="DEAL-100",
        predicted_profit=50000,
        actual_profit=55000,
    )

    assert feedback.deal_id == "DEAL-100"

    assert feedback.accuracy_score > 0

    history = engine.get_feedback_history()

    assert len(history) == 1