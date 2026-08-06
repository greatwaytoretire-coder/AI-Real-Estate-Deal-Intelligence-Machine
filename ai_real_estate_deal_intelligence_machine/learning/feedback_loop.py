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



class FeedbackLoop:
    """
    Autonomous learning feedback coordinator.

    Connects:

    Outcome Analysis
        |
        v
    Pattern Detection
        |
        v
    Scoring Adjustment

    """



    def __init__(self):

        self.outcome_analyzer = OutcomeAnalyzer()

        self.pattern_detector = PatternDetector()

        self.scoring_adjuster = ScoringAdjuster()



    def process(
        self,
        prediction: Dict[str, Any],
        actual: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run complete learning feedback cycle.
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


            "status":

                "LEARNING_COMPLETE",

        }



        print()

        print(
            "Learning Feedback Complete:"
        )

        print(
            feedback
        )



        return feedback