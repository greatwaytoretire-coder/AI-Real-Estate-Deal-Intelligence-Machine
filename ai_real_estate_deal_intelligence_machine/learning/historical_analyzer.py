from typing import Dict, Any, List


class HistoricalAnalyzer:
    """
    Historical deal performance analyzer.

    Sprint 4 Part 7:

    Converts previous deal outcomes into
    reusable investment intelligence.

    Flow:

    Deal History
        |
        v
    Outcome Analysis
        |
        v
    Pattern Extraction
        |
        v
    Confidence Signals
    """

    def __init__(self):
        self.minimum_history_required = 3


    def analyze(
        self,
        deal_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze historical investment outcomes.
        """


        if not deal_history:

            return {

                "status": "NO_HISTORY",

                "patterns": [],

                "confidence": 0,

                "message":
                    "No historical deal data available.",

            }


        if len(deal_history) < self.minimum_history_required:

            return {

                "status": "LIMITED_HISTORY",

                "patterns": [

                    "Additional deal history is required "
                    "to identify stronger investment patterns."

                ],

                "confidence": 10,

                "sample_size":
                    len(deal_history),

            }


        successful_deals = []

        failed_deals = []


        for deal in deal_history:

            if deal.get("status") == "SUCCESS":

                successful_deals.append(deal)

            else:

                failed_deals.append(deal)



        success_rate = (

            len(successful_deals)
            /
            len(deal_history)

        ) * 100



        average_roi = 0


        roi_values = [

            deal.get("roi", 0)

            for deal in deal_history

        ]


        if roi_values:

            average_roi = (

                sum(roi_values)
                /
                len(roi_values)

            )



        patterns = []



        if success_rate >= 75:

            patterns.append(

                "Historical acquisitions show strong "
                "positive performance."

            )


        elif success_rate < 50:

            patterns.append(

                "Historical acquisitions show elevated risk."

            )


        else:

            patterns.append(

                "Historical acquisitions show mixed performance."

            )



        return {


            "status":
                "ANALYSIS_COMPLETE",


            "sample_size":
                len(deal_history),


            "successful_deals":
                len(successful_deals),


            "failed_deals":
                len(failed_deals),


            "success_rate":
                round(success_rate, 2),


            "average_roi":
                round(average_roi, 2),


            "patterns":
                patterns,


            "confidence":
                min(len(deal_history) * 10, 100),

        }