from datetime import datetime, timezone
from typing import Dict, Any


from ai_real_estate_deal_intelligence_machine.learning.outcome_analyzer import (
    OutcomeAnalyzer,
)


from ai_real_estate_deal_intelligence_machine.learning.pattern_detector import (
    PatternDetector,
)


from ai_real_estate_deal_intelligence_machine.learning.scoring_adjuster import (
    ScoringAdjuster,
)


from ai_real_estate_deal_intelligence_machine.learning.adaptive_engine import (
    AdaptiveEngine,
)


from ai_real_estate_deal_intelligence_machine.learning.confidence_model import (
    ConfidenceModel,
)


from ai_real_estate_deal_intelligence_machine.learning.strategy_optimizer import (
    StrategyOptimizer,
)



class FeedbackLoop:
    """
    Autonomous learning feedback coordinator.

    Sprint 4 Part 5 Upgrade:

    Connects:

    Outcome Analysis
            |
            v
    Pattern Detection
            |
            v
    Scoring Adjustment
            |
            v
    Adaptive Intelligence
            |
            v
    Strategy Optimization

    """



    def __init__(self):

        self.outcome_analyzer = OutcomeAnalyzer()

        self.pattern_detector = PatternDetector()

        self.scoring_adjuster = ScoringAdjuster()


        # Sprint 4 Part 5 Adaptive Layer

        self.adaptive_engine = AdaptiveEngine()

        self.confidence_model = ConfidenceModel()

        self.strategy_optimizer = StrategyOptimizer()



    def process(
        self,
        prediction: Dict[str, Any],
        actual: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run complete autonomous learning feedback cycle.
        """



        print()

        print(
            "Running autonomous learning feedback loop..."
        )



        # ==========================================
        # STEP 1 - Analyze Outcome
        # ==========================================


        outcome_analysis = (

            self.outcome_analyzer.analyze(

                prediction,

                actual,

            )

        )



        # ==========================================
        # STEP 2 - Detect Patterns
        # ==========================================


        patterns = (

            self.pattern_detector.analyze(

                [

                    outcome_analysis

                ]

            )

        )



        # ==========================================
        # STEP 3 - Adjust Scoring
        # ==========================================


        adjustments = (

            self.scoring_adjuster.adjust(

                outcome_analysis.lessons

            )

        )



        # ==========================================
        # STEP 4 - Record Adaptive Learning
        # ==========================================


        self.adaptive_engine.record_learning(

            {

                "prediction":

                    prediction,


                "actual":

                    actual,


                "lessons":

                    outcome_analysis.lessons,

            }

        )



        # ==========================================
        # STEP 5 - Calculate Confidence
        # ==========================================


        confidence = (

            self.confidence_model.calculate(

                learning_events=len(

                    self.adaptive_engine.learning_history

                ),

                successful_events=1,

            )

        )



        # ==========================================
        # STEP 6 - Optimize Strategy
        # ==========================================


        strategy = (

            self.strategy_optimizer.optimize(

                confidence,

                patterns.get(

                    "patterns",

                    []

                ),

            )

        )



        feedback = {


            "processed_at":

                datetime.now(

                    timezone.utc

                ),


            "outcome_analysis":

                outcome_analysis,


            "patterns":

                patterns,


            "score_adjustments":

                adjustments,


            "adaptive_confidence":

                confidence,


            "strategy_optimization":

                strategy,


            "status":

                "ADAPTIVE_LEARNING_COMPLETE",

        }



        print()

        print(
            "Adaptive Learning Feedback Complete:"
        )

        print(
            feedback
        )



        return feedback