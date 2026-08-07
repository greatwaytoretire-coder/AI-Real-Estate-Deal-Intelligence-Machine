from ai_real_estate_deal_intelligence_machine.learning.closed_deal_tracker import (
    ClosedDealRecord,
    ClosedDealTracker,
)

from ai_real_estate_deal_intelligence_machine.learning.performance_evaluator import (
    PerformanceEvaluator,
)

from ai_real_estate_deal_intelligence_machine.learning.outcome_classifier import (
    OutcomeClassifier,
)

from ai_real_estate_deal_intelligence_machine.learning.learning_statistics import (
    LearningStatistics,
)

from ai_real_estate_deal_intelligence_machine.learning.retraining_engine import (
    RetrainingEngine,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 8 INTEGRATION TEST")
    print("CLOSED DEAL LEARNING")
    print("=" * 70)

    tracker = ClosedDealTracker()
    evaluator = PerformanceEvaluator()
    classifier = OutcomeClassifier()
    statistics_engine = LearningStatistics()
    retraining_engine = RetrainingEngine()

    print()
    print("STEP 1 - Recording Closed Deals")

    closed_deals = [
        ClosedDealRecord(
            deal_id="CLOSED-001",
            property_id="PROPERTY-001",
            purchase_price=150000,
            projected_profit=90000,
            actual_profit=105000,
            projected_roi=60.0,
            actual_roi=70.0,
            status="CLOSED",
            exit_strategy="WHOLESALE",
            notes="Successful wholesale exit.",
        ),
        ClosedDealRecord(
            deal_id="CLOSED-002",
            property_id="PROPERTY-002",
            purchase_price=120000,
            projected_profit=50000,
            actual_profit=42000,
            projected_roi=41.67,
            actual_roi=35.0,
            status="CLOSED",
            exit_strategy="WHOLESALE",
            notes="Profit below projection.",
        ),
        ClosedDealRecord(
            deal_id="CLOSED-003",
            property_id="PROPERTY-003",
            purchase_price=200000,
            projected_profit=75000,
            actual_profit=-15000,
            projected_roi=37.5,
            actual_roi=-7.5,
            status="CLOSED",
            exit_strategy="FLIP",
            notes="Unexpected repair and holding costs.",
        ),
    ]

    for deal in closed_deals:
        tracker.record(deal)

    print(
        f"Closed deals recorded: {tracker.count()}"
    )

    print()
    print("STEP 2 - Evaluating Deal Performance")

    outcomes = []

    for deal in tracker.get_all():
        performance = evaluator.evaluate(
            projected_profit=deal.projected_profit,
            actual_profit=deal.actual_profit,
            projected_roi=deal.projected_roi,
            actual_roi=deal.actual_roi,
        )

        classification = classifier.classify(
            actual_profit=deal.actual_profit,
            actual_roi=deal.actual_roi,
        )

        outcome = {
            "deal_id": deal.deal_id,
            "actual_profit": deal.actual_profit,
            "actual_roi": deal.actual_roi,
            "success": classification["success"],
            "category": classification["category"],
            "performance": performance,
        }

        outcomes.append(outcome)

        print()
        print(f"Deal: {deal.deal_id}")
        print("Performance:")
        print(performance)
        print("Classification:")
        print(classification)

    print()
    print("STEP 3 - Calculating Learning Statistics")

    statistics = statistics_engine.calculate(
        outcomes
    )

    print(statistics)

    print()
    print("STEP 4 - Running Retraining Engine")

    retraining = retraining_engine.retrain(
        outcomes=outcomes,
        statistics=statistics,
    )

    print(retraining)

    print()
    print("STEP 5 - Portfolio Summary")

    print(tracker.summary())

    print()
    print("=" * 70)
    print("SPRINT 4 PART 8 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()