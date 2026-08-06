from typing import Dict, Any


class DecisionModifier:
    """
    Applies learned intelligence adjustments
    to future investment decisions.
    """


    def apply(
        self,
        decision: Dict[str, Any],
        learning_rules: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Modify deal decisions using
        adaptive learning signals.
        """


        modified_decision = decision.copy()


        original_score = modified_decision.get(
            "deal_score",
            0
        )


        confidence = learning_rules.get(
            "confidence",
            0
        )


        adjustment = 0


        if confidence >= 50:

            adjustment += 5


        if confidence >= 75:

            adjustment += 5


        modified_score = min(
            original_score + adjustment,
            100
        )


        modified_decision["original_score"] = (
            original_score
        )


        modified_decision["learning_adjustment"] = (
            adjustment
        )


        modified_decision["adaptive_score"] = (
            modified_score
        )


        modified_decision["learning_confidence"] = (
            confidence
        )


        return modified_decision