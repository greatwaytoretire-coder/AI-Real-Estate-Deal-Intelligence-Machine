from __future__ import annotations

from typing import Any, Dict


class AcquisitionDecisionEngine:
    """
    Converts deal recommendations and confidence signals
    into an acquisition decision.

    Sprint 4 Part 15:
    Acquisition Decision Intelligence.

    Decision flow:

        Deal Recommendation
                |
                v
        Recommendation Confidence
                |
                v
        Acquisition Decision
                |
                v
        FINAL ACTION
    """

    def decide(
        self,
        recommendation_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate an acquisition decision from
        recommendation and confidence signals.
        """

        if not isinstance(
            recommendation_data,
            dict,
        ):
            return {
                "decision": "PASS",
                "action": "NO_ACTION",
                "confidence_level": "LOW",
                "status": "INVALID_RECOMMENDATION_DATA",
            }

        recommendation = str(
            recommendation_data.get(
                "recommendation",
                "PASS",
            )
        ).upper()

        confidence_level = str(
            recommendation_data.get(
                "confidence_level",
                recommendation_data.get(
                    "confidence",
                    "LOW",
                ),
            )
        ).upper()

        confidence_score = float(
            recommendation_data.get(
                "confidence_score",
                0.0,
            )
        )

        recommendation_score = float(
            recommendation_data.get(
                "recommendation_score",
                0.0,
            )
        )

        risk_level = str(
            recommendation_data.get(
                "risk_level",
                "HIGH",
            )
        ).upper()

        deal_id = recommendation_data.get(
            "deal_id",
            "UNKNOWN",
        )

        # --------------------------------------------------------------
        # Primary acquisition decision
        # --------------------------------------------------------------

        if (
            recommendation == "PURSUE"
            and confidence_level == "HIGH"
            and confidence_score >= 80
            and recommendation_score >= 70
            and risk_level == "LOW"
        ):
            decision = "ACQUIRE"
            action = "PROCEED_TO_ACQUISITION"

        elif (
            recommendation == "PURSUE"
            and confidence_score >= 65
            and recommendation_score >= 60
            and risk_level in {
                "LOW",
                "MEDIUM",
            }
        ):
            decision = "REVIEW"
            action = "REQUIRE_ADDITIONAL_DUE_DILIGENCE"

        elif (
            recommendation == "WATCH"
            or (
                recommendation_score >= 45
                and confidence_score >= 50
            )
        ):
            decision = "MONITOR"
            action = "CONTINUE_MARKET_MONITORING"

        else:
            decision = "PASS"
            action = "NO_ACTION"

        return {
            "deal_id": deal_id,
            "decision": decision,
            "action": action,
            "recommendation": recommendation,
            "recommendation_score": round(
                recommendation_score,
                2,
            ),
            "confidence_score": round(
                confidence_score,
                2,
            ),
            "confidence_level": confidence_level,
            "risk_level": risk_level,
            "status": "ACQUISITION_DECISION_GENERATED",
        }