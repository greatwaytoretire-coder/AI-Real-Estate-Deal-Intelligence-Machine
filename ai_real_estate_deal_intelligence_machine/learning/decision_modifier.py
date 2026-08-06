from typing import Dict, Any


class DecisionModifier:
    """
    Adaptive decision modification engine.

    Adjusts investment decisions using
    accumulated learning signals.
    """



    def __init__(self):

        self.minimum_score = 0

        self.maximum_score = 100



    def modify(
        self,
        decision_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Modify a deal recommendation using
        adaptive intelligence rules.
        """

        original_score = decision_data.get(
            "deal_score",
            0,
        )


        recommendation = decision_data.get(
            "recommendation",
            "REVIEW",
        )


        risk_level = decision_data.get(
            "risk_level",
            "UNKNOWN",
        )


        profit_margin = decision_data.get(
            "profit_margin",
            0,
        )



        adjusted_score = original_score



        reasoning = []



        # Strong profit margin reinforcement

        if profit_margin >= 50:

            adjusted_score += 5

            reasoning.append(
                "High profit margin increased confidence."
            )



        # Risk adjustment

        if risk_level == "LOW":

            adjusted_score += 5

            reasoning.append(
                "Low risk profile increased confidence."
            )


        elif risk_level == "HIGH":

            adjusted_score -= 10

            reasoning.append(
                "High risk profile reduced confidence."
            )



        # Clamp score

        adjusted_score = max(

            self.minimum_score,

            min(
                adjusted_score,
                self.maximum_score,
            ),

        )



        # Update recommendation

        if adjusted_score >= 85:

            recommendation = "ACQUIRE"


        elif adjusted_score >= 65:

            recommendation = "REVIEW"


        else:

            recommendation = "PASS"



        return {


            "original_score":

                original_score,


            "adjusted_score":

                adjusted_score,


            "recommendation":

                recommendation,


            "reasoning":

                reasoning,


            "status":

                "ADAPTIVE_DECISION_COMPLETE",

        }