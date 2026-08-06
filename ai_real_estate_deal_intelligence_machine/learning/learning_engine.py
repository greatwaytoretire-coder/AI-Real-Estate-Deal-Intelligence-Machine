from datetime import datetime, timezone


class LearningEngine:
    """
    Autonomous learning engine.

    Stores deal outcomes and generates
    improvement signals for future analysis.
    """


    def __init__(self):

        self.records = []



    def record_outcome(
        self,
        deal_id,
        recommendation,
        projected_profit,
        roi,
        status,
    ):

        record = {

            "deal_id":
                deal_id,

            "recommendation":
                recommendation,

            "projected_profit":
                projected_profit,

            "roi":
                roi,

            "status":
                status,

            "recorded_at":
                datetime.now(
                    timezone.utc
                ),

        }


        self.records.append(
            record
        )


        return record



    def analyze_performance(self):

        if not self.records:

            return {

                "total_deals":
                    0,

                "success_rate":
                    0,

                "average_roi":
                    0,

            }



        total = len(
            self.records
        )


        successful = len(

            [

                r for r in self.records

                if r["status"]
                ==
                "COMPLETED"

            ]

        )


        average_roi = sum(

            r["roi"]

            for r in self.records

        ) / total



        return {


            "total_deals":
                total,


            "successful_deals":
                successful,


            "success_rate":
                round(
                    successful / total * 100,
                    2
                ),


            "average_roi":
                round(
                    average_roi,
                    2
                ),


        }
    