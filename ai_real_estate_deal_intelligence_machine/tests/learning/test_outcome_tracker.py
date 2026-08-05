from ai_real_estate_deal_intelligence_machine.learning.outcome_tracker import (
    OutcomeTracker,
)


def test_outcome_tracker_records_learning():

    tracker = OutcomeTracker()

    outcome = tracker.record_outcome(
        deal_id="DEAL-001",
        address="123 Main Street",
        outcome="CLOSED",
        actual_profit=50000,
        expected_profit=40000,
    )

    assert outcome.deal_id == "DEAL-001"

    history = tracker.get_learning_history()

    assert len(history) == 1
    assert "exceeded" in history[0].lesson