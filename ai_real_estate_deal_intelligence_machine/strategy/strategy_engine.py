from datetime import datetime, timezone

from .strategy_models import StrategyRecommendation


class StrategyEngine:

    def recommend_strategy(
        self,
        property_id,
        roi,
        repair_cost_ratio,
    ):

        if roi >= 0.25 and repair_cost_ratio < 0.20:
            strategy = "FIX_AND_FLIP"
            confidence = 0.95
            notes = "High ROI with manageable repairs."

        elif roi >= 0.15:
            strategy = "BUY_AND_HOLD"
            confidence = 0.90
            notes = "Strong long-term investment."

        elif roi >= 0.08:
            strategy = "WHOLESALE"
            confidence = 0.80
            notes = "Suitable for assignment."

        else:
            strategy = "REVIEW_REQUIRED"
            confidence = 0.50
            notes = "Requires manual review."

        return StrategyRecommendation(
            property_id=property_id,
            strategy=strategy,
            confidence=confidence,
            notes=notes,
            created_at=datetime.now(timezone.utc),
        )