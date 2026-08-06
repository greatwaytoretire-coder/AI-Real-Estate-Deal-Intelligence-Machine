from typing import Dict, Any


class ConfidenceModel:
    """
    Evaluates confidence levels from historical
    learning performance.

    Sprint 4 Part 5:

    Learning Data
          |
          v
    Confidence Score
          |
          v
    Adaptive Decisions
    """

    def calculate(
        self,
        learning_events: int,
        successful_events: int,
    ) -> Dict[str, Any]:
        """
        Calculate learning confidence.

        Confidence is based on:
        - amount of historical data
        - success ratio
        """

        if learning_events == 0:

            return {

                "confidence_score": 0,

                "success_rate": 0,

                "status": "INSUFFICIENT_DATA",

            }



        success_rate = (

            successful_events
            /
            learning_events

        ) * 100



        data_strength = min(
            learning_events * 10,
            100,
        )



        confidence_score = (

            success_rate
            *
            0.7

            +

            data_strength
            *
            0.3

        )



        if confidence_score >= 80:

            status = "HIGH_CONFIDENCE"


        elif confidence_score >= 50:

            status = "MODERATE_CONFIDENCE"


        else:

            status = "LOW_CONFIDENCE"



        return {

            "confidence_score":
                round(confidence_score, 2),

            "success_rate":
                round(success_rate, 2),

            "data_points":
                learning_events,

            "status":
                status,

        }
    