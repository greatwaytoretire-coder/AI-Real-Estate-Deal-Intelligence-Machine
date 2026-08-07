from __future__ import annotations

from typing import Any, Dict, List, Optional


class PredictionMemory:
    """
    Stores predictive intelligence records.

    Sprint 4 Part 12:
    Continuous Intelligence Optimization.

    This memory layer stores predictions so the system
    can later compare predictions against actual outcomes.
    """

    def __init__(self) -> None:
        self._predictions: List[Dict[str, Any]] = []

    def store(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store a prediction record.
        """

        self._predictions.append(prediction)

        return prediction

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Return all stored predictions.
        """

        return list(self._predictions)

    def find_by_deal(
        self,
        deal_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Find prediction by deal ID.
        """

        for prediction in self._predictions:
            if prediction.get("deal_id") == deal_id:
                return prediction

        return None

    def count(self) -> int:
        """
        Return number of predictions stored.
        """

        return len(self._predictions)

    def summary(self) -> Dict[str, Any]:
        """
        Return prediction memory summary.
        """

        return {
            "total_predictions": len(
                self._predictions
            ),
            "status": "PREDICTION_MEMORY_READY",
        }
    