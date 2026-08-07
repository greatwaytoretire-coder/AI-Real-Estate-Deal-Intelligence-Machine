from __future__ import annotations

from typing import Any, Dict

from ai_real_estate_deal_intelligence_machine.learning.deal_outcome_predictor import (
    DealOutcomePredictor,
)

from ai_real_estate_deal_intelligence_machine.learning.predictive_signal_engine import (
    PredictiveSignalEngine,
)


class PredictiveIntelligenceEngine:
    """
    Coordinates predictive investment intelligence.

    Sprint 4 Part 11:
    Predictive Deal Intelligence.

    Combines:

    Market intelligence
    Closed deal learning
    Predictive signals
    Outcome prediction

    into a future investment recommendation.
    """

    def __init__(self) -> None:

        self.signal_engine = PredictiveSignalEngine()

        self.outcome_predictor = DealOutcomePredictor()


    def analyze(
        self,
        deal_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate predictive investment intelligence.
        """

        signals = self.signal_engine.analyze(
            deal_data
        )


        prediction = self.outcome_predictor.predict(
            {
                "deal_id":
                    deal_data.get(
                        "deal_id",
                        "UNKNOWN",
                    ),

                "deal_score":
                    signals["signals_used"].get(
                        "deal_score",
                        0,
                    ),

                "market_confidence":
                    signals["signals_used"].get(
                        "market_confidence",
                        0,
                    ),

                "profit_margin":
                    deal_data.get(
                        "profit_margin",
                        0,
                    ),

                "risk_level":
                    deal_data.get(
                        "risk_level",
                        "UNKNOWN",
                    ),
            }
        )


        return {

            "signals":
                signals,

            "prediction":
                prediction,

            "recommendation":
                signals["recommendation"],

            "status":
                "PREDICTIVE_INTELLIGENCE_COMPLETE",

        }