from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class LearningFeedback:
    """
    Connects closed deal learning results back into
    future investment intelligence.

    Sprint 4 Part 9:
    Learning Intelligence Integration.

    Creates the final adaptive feedback loop.
    """

    def apply(
        self,
        deal_id: str,
        confidence_result: Dict[str, Any],
        strategy_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Combine strategy optimization and confidence
        adjustment into future learning guidance.
        """

        return {

            "deal_id":
                deal_id,

            "confidence":
                confidence_result,

            "strategy":
                strategy_result,

            "learning_status":
                "FEEDBACK_APPLIED",

            "recommendations":
                strategy_result.get(
                    "recommendations",
                    [],
                ),

            "updated_at":
                datetime.now(
                    timezone.utc
                ),

        }