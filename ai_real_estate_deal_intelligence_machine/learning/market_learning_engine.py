from __future__ import annotations

from typing import Any, Dict, Iterable


from ai_real_estate_deal_intelligence_machine.learning.market_memory import (
    MarketMemory,
)


from ai_real_estate_deal_intelligence_machine.learning.market_pattern_detector import (
    MarketPatternDetector,
)


from ai_real_estate_deal_intelligence_machine.learning.market_confidence_model import (
    MarketConfidenceModel,
)



class MarketLearningEngine:
    """
    Coordinates market-level investment intelligence.

    Sprint 4 Part 10:
    Market Intelligence Learning Engine.

    Flow:

    Market Memory
          |
          v
    Pattern Detection
          |
          v
    Confidence Evaluation
          |
          v
    Market Recommendation
    """

    def __init__(self) -> None:

        self.market_memory = MarketMemory()

        self.pattern_detector = MarketPatternDetector()

        self.confidence_model = MarketConfidenceModel()



    def learn(
        self,
        market_records: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze historical market intelligence.
        """


        for record in market_records:

            self.market_memory.store(
                record
            )


        stored_markets = (
            self.market_memory.get_all()
        )


        patterns = (
            self.pattern_detector.analyze(
                stored_markets
            )
        )


        confidence_results = []


        for market in stored_markets:

            confidence_results.append(

                self.confidence_model.evaluate(
                    market
                )

            )


        recommendations = []


        for result in confidence_results:

            if result["confidence_level"] == "HIGH":

                recommendations.append(

                    f"{result['market']} "
                    "is a high-confidence investment market."

                )

            elif result["confidence_level"] == "MEDIUM":

                recommendations.append(

                    f"{result['market']} "
                    "requires additional monitoring."

                )

            else:

                recommendations.append(

                    f"{result['market']} "
                    "has insufficient historical confidence."

                )



        return {

            "status":
                "MARKET_LEARNING_COMPLETE",

            "market_memory":
                self.market_memory.summary(),

            "patterns":
                patterns,

            "confidence_results":
                confidence_results,

            "recommendations":
                recommendations,

        }