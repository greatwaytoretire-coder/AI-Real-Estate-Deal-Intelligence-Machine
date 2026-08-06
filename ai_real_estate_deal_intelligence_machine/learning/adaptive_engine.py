from typing import Dict, Any


from ai_real_estate_deal_intelligence_machine.learning.confidence_model import (
    ConfidenceModel,
)


from ai_real_estate_deal_intelligence_machine.learning.strategy_optimizer import (
    StrategyOptimizer,
)


from ai_real_estate_deal_intelligence_machine.learning.learning_memory import (
    LearningMemory,
)



class AdaptiveEngine:
    """
    Adaptive investment intelligence engine.

    Sprint 4 Part 7:

    Uses historical experience to improve
    future acquisition decisions.

    Flow:

    Current Deal
        |
        v
    Historical Memory
        |
        v
    Confidence Model
        |
        v
    Strategy Optimization
        |
        v
    Adaptive Decision
    """



    def __init__(self):

        self.confidence_model = ConfidenceModel()

        self.strategy_optimizer = StrategyOptimizer()

        self.learning_memory = LearningMemory()



    def evaluate(
        self,
        deal: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate a deal using learned experience.
        """



        historical_summary = (

            self.learning_memory.analyze_history()

        )



        confidence_adjustment = (

            self.confidence_model.evaluate(

                deal,

                historical_summary,

            )

        )



        strategy_result = (

            self.strategy_optimizer.optimize(

                deal,

                historical_summary,

            )

        )



        original_score = (

            deal.get(

                "deal_score",

                0

            )

        )



        adjusted_score = (

            original_score

            +

            confidence_adjustment.get(

                "adjustment",

                0

            )

        )



        adjusted_score = max(

            0,

            min(

                adjusted_score,

                100

            )

        )



        recommendation = (

            "ACQUIRE"

            if adjusted_score >= 75

            else "REVIEW"

        )



        return {


            "original_score":

                original_score,


            "adjusted_score":

                adjusted_score,


            "recommendation":

                recommendation,


            "historical_analysis":

                historical_summary,


            "confidence":

                confidence_adjustment,


            "strategy":

                strategy_result,


            "status":

                "ADAPTIVE_ANALYSIS_COMPLETE",

        }