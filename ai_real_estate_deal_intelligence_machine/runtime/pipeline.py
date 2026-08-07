from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from ai_real_estate_deal_intelligence_machine.runtime.deal_context import (
    DealContext,
)

from ai_real_estate_deal_intelligence_machine.acquisition.seller_lead_pipeline import (
    SellerLeadPipeline,
)

from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)

from ai_real_estate_deal_intelligence_machine.matching.buyer_matching_engine import (
    BuyerMatchingEngine,
)

from ai_real_estate_deal_intelligence_machine.deal_packaging.deal_package_generator import (
    DealPackageGenerator,
)

from ai_real_estate_deal_intelligence_machine.execution.deal_execution_engine import (
    DealExecutionEngine,
)

from ai_real_estate_deal_intelligence_machine.database.models import (
    DealRecord,
)

from ai_real_estate_deal_intelligence_machine.database.deal_repository import (
    DealRepository,
)

from ai_real_estate_deal_intelligence_machine.learning.learning_models import (
    LearningRecord,
)

from ai_real_estate_deal_intelligence_machine.learning.learning_repository import (
    LearningRepository,
)

from ai_real_estate_deal_intelligence_machine.learning.pattern_detector import (
    PatternDetector,
)

from ai_real_estate_deal_intelligence_machine.learning.learning_memory import (
    LearningMemory,
)

from ai_real_estate_deal_intelligence_machine.learning.adaptive_engine import (
    AdaptiveEngine,
)

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


class AutonomousPipeline:
    """
    Autonomous real estate investment intelligence pipeline.

    Sprint 4 Part 8 Upgrade:

    Adds closed-deal learning capabilities while preserving the
    existing Sprint 4 Part 7 historical adaptive intelligence.

    LIVE DEAL FLOW:

        Seller Analysis
              |
              v
        Deal Intelligence
              |
              v
        Historical Adaptive Learning
              |
              v
        Adaptive Decision Engine
              |
              v
        Buyer Matching
              |
              v
        Deal Packaging
              |
              v
        Execution Readiness
              |
              v
        Deal Memory

    CLOSED DEAL LEARNING FLOW:

        Actual Closed Deal
              |
              v
        Performance Evaluation
              |
              v
        Outcome Classification
              |
              v
        Learning Statistics
              |
              v
        Retraining Engine
              |
              v
        Future Adaptive Intelligence
    """

    def __init__(self) -> None:
        # ---------------------------------------------------------
        # Core Investment Pipeline
        # ---------------------------------------------------------

        self.seller_pipeline = SellerLeadPipeline()

        self.intelligence = DealIntelligenceCoordinator()

        self.buyer_matching = BuyerMatchingEngine()

        self.package_generator = DealPackageGenerator()

        self.execution = DealExecutionEngine()

        self.deal_repository = DealRepository()

        # ---------------------------------------------------------
        # Existing Learning System
        # ---------------------------------------------------------

        self.learning_repository = LearningRepository()

        self.pattern_detector = PatternDetector()

        self.learning_memory = LearningMemory()

        # ---------------------------------------------------------
        # Existing Adaptive Intelligence
        # ---------------------------------------------------------

        self.adaptive_engine = AdaptiveEngine()

        # ---------------------------------------------------------
        # Sprint 4 Part 8 - Closed Deal Learning
        # ---------------------------------------------------------

        self.closed_deal_tracker = ClosedDealTracker()

        self.performance_evaluator = PerformanceEvaluator()

        self.outcome_classifier = OutcomeClassifier()

        self.learning_statistics = LearningStatistics()

        self.retraining_engine = RetrainingEngine()

    # =================================================================
    # LIVE DEAL ANALYSIS
    # =================================================================

    def execute(
        self,
        context: DealContext,
    ) -> Dict[str, Any]:
        """
        Execute the complete live investment analysis pipeline.

        This method evaluates an opportunity and prepares it for
        execution. It does NOT assume that the transaction has
        financially closed.
        """

        print("=" * 70)
        print("AUTONOMOUS INVESTMENT ANALYSIS STARTED")
        print("=" * 70)

        # ---------------------------------------------------------
        # STEP 1 - Seller Opportunity Analysis
        # ---------------------------------------------------------

        print(
            "\nSTEP 1 - Seller Opportunity Analysis"
        )

        seller_results = self.seller_pipeline.analyze_lead(
            market=context.opportunity["market"],
            property_address=context.opportunity["property_address"],
            estimated_value=context.opportunity["estimated_value"],
            motivation_score=context.opportunity["motivation_score"],
            distress_signals=context.opportunity["distress_signals"],
        )

        print(seller_results)

        # ---------------------------------------------------------
        # STEP 2 - Deal Intelligence Analysis
        # ---------------------------------------------------------

        print(
            "\nSTEP 2 - Deal Intelligence Analysis"
        )

        intelligence_result = self.intelligence.analyze(
            property_id=context.deal_id,
            purchase_price=150000,
            estimated_value=context.opportunity["estimated_value"],
            repair_cost=35000,
        )

        print(intelligence_result)

        # ---------------------------------------------------------
        # STEP 3 - Historical Adaptive Learning
        # ---------------------------------------------------------

        print(
            "\nSTEP 3 - Historical Adaptive Learning"
        )

        roi_percentage = (
            intelligence_result.projected_profit
            / intelligence_result.purchase_price
            * 100
        )

        adaptive_result = self.adaptive_engine.evaluate(
            {
                "deal_score": intelligence_result.deal_score,
                "projected_profit": (
                    intelligence_result.projected_profit
                ),
                "risk_level": intelligence_result.risk_level,
                "roi": roi_percentage,
            }
        )

        print(adaptive_result)

        # ---------------------------------------------------------
        # STEP 4 - Buyer Matching
        # ---------------------------------------------------------

        print(
            "\nSTEP 4 - Buyer Matching"
        )

        buyers = [
            {
                "buyer_id": "BUYER-001",
                "buyer_name": "Detroit Cash Investors",
                "preferred_markets": ["Detroit"],
                "preferred_property_types": [
                    "single_family"
                ],
                "investment_score": 95,
            },
            {
                "buyer_id": "BUYER-002",
                "buyer_name": "Midwest Rental Group",
                "preferred_markets": ["Detroit"],
                "preferred_property_types": [
                    "multi_family"
                ],
                "investment_score": 85,
            },
        ]

        buyer_matches = self.buyer_matching.match(
            buyers=buyers,
            deal={
                "market": context.opportunity["market"],
                "property_type": "single_family",
            },
        )

        print(buyer_matches)

        # ---------------------------------------------------------
        # STEP 5 - Deal Package Generation
        # ---------------------------------------------------------

        print(
            "\nSTEP 5 - Deal Package Generation"
        )

        underwriting = {
            "property_id": intelligence_result.property_id,
            "address": context.opportunity["property_address"],
            "arv": intelligence_result.estimated_value,
            "purchase_price": intelligence_result.purchase_price,
            "repair_cost": intelligence_result.repair_cost,
            "projected_profit": (
                intelligence_result.projected_profit
            ),
            "roi_percentage": roi_percentage,
            "recommendation": adaptive_result["recommendation"],
            "deal_score": adaptive_result["adjusted_score"],
            "risk_level": intelligence_result.risk_level,
        }

        buyer_data = []

        for buyer in buyer_matches:
            buyer_data.append(
                {
                    "buyer_id": buyer.buyer_id,
                    "buyer_name": buyer.buyer_name,
                    "score": buyer.score,
                    "recommendation": buyer.recommendation,
                    "reasoning": buyer.reasoning,
                }
            )

        package = self.package_generator.generate(
            underwriting,
            buyer_data,
        )

        print(package)

        # ---------------------------------------------------------
        # STEP 6 - Execution Readiness
        # ---------------------------------------------------------

        print(
            "\nSTEP 6 - Execution Readiness"
        )

        execution_result = self.execution.execute(
            package
        )

        print(execution_result)

        # ---------------------------------------------------------
        # STEP 7 - Saving Deal Memory
        # ---------------------------------------------------------

        print(
            "\nSTEP 7 - Saving Deal Memory"
        )

        deal_record = DealRecord(
            deal_id=context.deal_id,
            property_id=intelligence_result.property_id,
            seller_id=seller_results[0].seller_id,
            recommendation=underwriting["recommendation"],
            deal_score=underwriting["deal_score"],
            projected_profit=(
                intelligence_result.projected_profit
            ),
            roi=roi_percentage,
            risk_level=intelligence_result.risk_level,
            status="COMPLETED",
        )

        self.deal_repository.save_deal(
            deal_record
        )

        print(deal_record)

        # ---------------------------------------------------------
        # STEP 8 - Learning Memory Update
        # ---------------------------------------------------------

        print(
            "\nSTEP 8 - Learning Memory Update"
        )

        learning_record = LearningRecord(
            deal_id=context.deal_id,
            lesson=(
                "Historical adaptive intelligence updated "
                "investment confidence."
            ),
            category="HISTORICAL_ADAPTIVE_LEARNING",
            created_at=datetime.now(timezone.utc),
        )

        self.learning_repository.save(
            learning_record
        )

        self.learning_memory.store(
            {
                "deal_id": context.deal_id,
                "status": "ANALYZED",
                "roi": roi_percentage,
                "deal_score": underwriting["deal_score"],
            }
        )

        patterns = self.pattern_detector.analyze(
            self.learning_repository.get_all()
        )

        print(patterns)

        print("=" * 70)
        print(
            "AUTONOMOUS INVESTMENT ANALYSIS COMPLETE"
        )
        print("=" * 70)

        return {
            "deal_id": context.deal_id,
            "seller_analysis": seller_results,
            "investment_analysis": intelligence_result,
            "adaptive_learning": adaptive_result,
            "buyer_matches": buyer_matches,
            "deal_package": package,
            "execution": execution_result,
            "stored_deal": deal_record,
            "learning_record": learning_record,
            "patterns": patterns,
            "recommendation": underwriting["recommendation"],
            "status": "COMPLETED",
        }

    # =================================================================
    # SPRINT 4 PART 8 - CLOSED DEAL LEARNING
    # =================================================================

    def record_closed_deal(
        self,
        deal_id: str,
        property_id: str,
        purchase_price: float,
        projected_profit: float,
        actual_profit: float,
        projected_roi: float,
        actual_roi: float,
        status: str = "CLOSED",
        exit_strategy: str = "UNKNOWN",
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Record and learn from an actual closed transaction.

        IMPORTANT:

        This method requires actual realized financial results.

        The pipeline never treats projected profit as actual profit.

        That distinction prevents the learning engine from training
        itself on hypothetical results.
        """

        print("=" * 70)
        print("CLOSED DEAL LEARNING STARTED")
        print("=" * 70)

        # ---------------------------------------------------------
        # STEP 1 - Record Actual Closed Deal
        # ---------------------------------------------------------

        print(
            "\nCLOSED LEARNING STEP 1 - Recording Closed Deal"
        )

        closed_deal = ClosedDealRecord(
            deal_id=deal_id,
            property_id=property_id,
            purchase_price=float(purchase_price),
            projected_profit=float(projected_profit),
            actual_profit=float(actual_profit),
            projected_roi=float(projected_roi),
            actual_roi=float(actual_roi),
            status=status,
            exit_strategy=exit_strategy,
            notes=notes,
        )

        self.closed_deal_tracker.record(
            closed_deal
        )

        print(closed_deal)

        # ---------------------------------------------------------
        # STEP 2 - Performance Evaluation
        # ---------------------------------------------------------

        print(
            "\nCLOSED LEARNING STEP 2 - Performance Evaluation"
        )

        performance = self.performance_evaluator.evaluate(
            projected_profit=closed_deal.projected_profit,
            actual_profit=closed_deal.actual_profit,
            projected_roi=closed_deal.projected_roi,
            actual_roi=closed_deal.actual_roi,
        )

        print(performance)

        # ---------------------------------------------------------
        # STEP 3 - Outcome Classification
        # ---------------------------------------------------------

        print(
            "\nCLOSED LEARNING STEP 3 - Outcome Classification"
        )

        classification = self.outcome_classifier.classify(
            actual_profit=closed_deal.actual_profit,
            actual_roi=closed_deal.actual_roi,
        )

        print(classification)

        # ---------------------------------------------------------
        # STEP 4 - Build Learning Outcome
        # ---------------------------------------------------------

        learning_outcome = {
            "deal_id": closed_deal.deal_id,
            "property_id": closed_deal.property_id,
            "actual_profit": closed_deal.actual_profit,
            "actual_roi": closed_deal.actual_roi,
            "success": classification["success"],
            "category": classification["category"],
            "performance": performance,
            "classification": classification,
        }

        # ---------------------------------------------------------
        # STEP 5 - Learning Statistics
        # ---------------------------------------------------------

        print(
            "\nCLOSED LEARNING STEP 4 - Learning Statistics"
        )

        all_closed_deals = (
            self.closed_deal_tracker.get_all()
        )

        all_outcomes = []

        for historical_deal in all_closed_deals:
            historical_classification = (
                self.outcome_classifier.classify(
                    actual_profit=historical_deal.actual_profit,
                    actual_roi=historical_deal.actual_roi,
                )
            )

            historical_performance = (
                self.performance_evaluator.evaluate(
                    projected_profit=(
                        historical_deal.projected_profit
                    ),
                    actual_profit=(
                        historical_deal.actual_profit
                    ),
                    projected_roi=(
                        historical_deal.projected_roi
                    ),
                    actual_roi=(
                        historical_deal.actual_roi
                    ),
                )
            )

            all_outcomes.append(
                {
                    "deal_id": historical_deal.deal_id,
                    "property_id": historical_deal.property_id,
                    "actual_profit": (
                        historical_deal.actual_profit
                    ),
                    "actual_roi": (
                        historical_deal.actual_roi
                    ),
                    "success": (
                        historical_classification["success"]
                    ),
                    "category": (
                        historical_classification["category"]
                    ),
                    "performance": historical_performance,
                    "classification": (
                        historical_classification
                    ),
                }
            )

        statistics = self.learning_statistics.calculate(
            all_outcomes
        )

        print(statistics)

        # ---------------------------------------------------------
        # STEP 6 - Retraining / Strategy Optimization
        # ---------------------------------------------------------

        print(
            "\nCLOSED LEARNING STEP 5 - Retraining Engine"
        )

        retraining = self.retraining_engine.retrain(
            outcomes=all_outcomes,
            statistics=statistics,
        )

        print(retraining)

        # ---------------------------------------------------------
        # STEP 7 - Store Learning Memory
        # ---------------------------------------------------------

        self.learning_memory.store(
            {
                "deal_id": deal_id,
                "status": "CLOSED",
                "actual_profit": (
                    closed_deal.actual_profit
                ),
                "actual_roi": (
                    closed_deal.actual_roi
                ),
                "outcome": (
                    classification["category"]
                ),
                "performance": performance,
                "statistics": statistics,
                "retraining": retraining,
                "recorded_at": datetime.now(
                    timezone.utc
                ),
            }
        )

        # ---------------------------------------------------------
        # STEP 8 - Persist Learning Record
        # ---------------------------------------------------------

        learning_record = LearningRecord(
            deal_id=deal_id,
            lesson=classification["lesson"],
            category="CLOSED_DEAL_LEARNING",
            created_at=datetime.now(timezone.utc),
        )

        self.learning_repository.save(
            learning_record
        )

        # ---------------------------------------------------------
        # Final Result
        # ---------------------------------------------------------

        result = {
            "deal_id": deal_id,
            "closed_deal": closed_deal,
            "performance": performance,
            "classification": classification,
            "statistics": statistics,
            "retraining": retraining,
            "learning_record": learning_record,
            "status": "CLOSED_DEAL_LEARNING_COMPLETE",
        }

        print()
        print("=" * 70)
        print(
            "CLOSED DEAL LEARNING COMPLETE"
        )
        print("=" * 70)

        return result