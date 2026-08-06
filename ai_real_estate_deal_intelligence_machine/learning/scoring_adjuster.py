from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class ScoreAdjustment:
    """
    Represents an AI scoring model adjustment.
    """

    category: str

    old_weight: float

    new_weight: float

    reason: str

    adjusted_at: datetime



class ScoringAdjuster:
    """
    Adjusts investment scoring weights based
    on historical learning outcomes.

    This is the foundation for adaptive
    underwriting intelligence.
    """



    def __init__(self):

        self.weights = {

            "profit_margin": 40.0,

            "seller_motivation": 30.0,

            "market_strength": 20.0,

            "risk": 10.0,

        }



    def adjust(
        self,
        lessons: List[str],
    ) -> List[ScoreAdjustment]:

        adjustments = []



        for lesson in lessons:



            if "distressed sellers" in lesson.lower():

                old = self.weights[
                    "seller_motivation"
                ]


                new = min(
                    old + 5,
                    50,
                )


                self.weights[
                    "seller_motivation"
                ] = new



                adjustments.append(

                    ScoreAdjustment(

                        category="seller_motivation",

                        old_weight=old,

                        new_weight=new,

                        reason=lesson,

                        adjusted_at=datetime.now(
                            timezone.utc
                        ),

                    )

                )



            if "profit projections" in lesson.lower():

                old = self.weights[
                    "profit_margin"
                ]


                new = min(
                    old + 5,
                    50,
                )


                self.weights[
                    "profit_margin"
                ] = new



                adjustments.append(

                    ScoreAdjustment(

                        category="profit_margin",

                        old_weight=old,

                        new_weight=new,

                        reason=lesson,

                        adjusted_at=datetime.now(
                            timezone.utc
                        ),

                    )

                )



        return adjustments



    def get_weights(self) -> Dict[str, float]:

        return self.weights