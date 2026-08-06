from typing import Dict, Any


class AdaptationRules:
    """
    Converts learned investment outcomes
    into adaptive decision rules.
    """


    def evaluate(
        self,
        memory: Dict[str, Any],
    ) -> Dict[str, Any]:

        rules = []


        outcome = memory.get(
            "outcome"
        )


        deal_score = memory.get(
            "deal_score",
            0
        )


        projected_profit = memory.get(
            "projected_profit",
            0
        )


        if (
            outcome == "SUCCESS"
            and deal_score >= 85
        ):

            rules.append(
                "Increase confidence for high scoring acquisitions."
            )


        if projected_profit >= 50000:

            rules.append(
                "Prioritize deals with strong profit margins."
            )


        if not rules:

            rules.append(
                "Insufficient learning data. Maintain baseline scoring."
            )


        return {

            "rules":
                rules,


            "confidence":

                min(
                    len(rules) * 25,
                    100
                ),

        }