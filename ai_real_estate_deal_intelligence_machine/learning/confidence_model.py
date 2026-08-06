from typing import Dict, Any, List


class ConfidenceModel:
    """
    Adaptive confidence scoring engine.

    Accepts:
    - historical learning records
    - numeric scores
    - deal intelligence dictionaries

    Sprint 4 Adaptive Intelligence Layer.
    """

    def __init__(self):

        self.base_confidence = 50



    def evaluate(
        self,
        historical_data: List[Any],
        current_score: Any,
    ) -> Dict[str, Any]:
        """
        Evaluate adaptive confidence.
        """

        confidence = self.base_confidence

        reasoning = []



        # ==========================================
        # Normalize Current Score Input
        # ==========================================

        if isinstance(current_score, dict):

            deal_score = current_score.get(
                "deal_score",
                current_score.get(
                    "score",
                    0,
                ),
            )

        else:

            deal_score = current_score



        try:

            deal_score = float(
                deal_score
            )

        except:

            deal_score = 0



        # ==========================================
        # Historical Pattern Analysis
        # ==========================================

        successful_patterns = 0



        for record in historical_data or []:


            category = None



            if isinstance(record, dict):

                category = record.get(
                    "category"
                )


            elif hasattr(
                record,
                "category",
            ):

                category = record.category


            elif isinstance(
                record,
                str,
            ):

                category = record



            if category and any(

                keyword in str(category).upper()

                for keyword in [

                    "SUCCESS",

                    "ADAPTIVE",

                    "ACQUISITION",

                ]

            ):

                successful_patterns += 1



        if successful_patterns:


            confidence += min(

                successful_patterns * 5,

                25,

            )


            reasoning.append(

                "Historical learning patterns increased confidence."

            )


        else:

            reasoning.append(

                "Limited historical learning patterns available."

            )



        # ==========================================
        # Deal Score Evaluation
        # ==========================================


        if deal_score >= 90:


            confidence += 20


            reasoning.append(

                "Exceptional deal score increased confidence."

            )


        elif deal_score >= 75:


            confidence += 10


            reasoning.append(

                "Strong deal score increased confidence."

            )


        else:


            confidence -= 10


            reasoning.append(

                "Lower deal score reduced confidence."

            )



        confidence = max(

            0,

            min(

                confidence,

                100,

            ),

        )



        return {


            "confidence_score":

                confidence,


            "confidence_level":

                (
                    "HIGH"

                    if confidence >= 80

                    else

                    "MEDIUM"

                    if confidence >= 50

                    else

                    "LOW"
                ),


            "reasoning":

                reasoning,


            "status":

                "CONFIDENCE_EVALUATED",

        }