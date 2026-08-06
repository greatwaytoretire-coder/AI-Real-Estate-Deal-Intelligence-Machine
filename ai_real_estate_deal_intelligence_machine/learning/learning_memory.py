from typing import Dict, Any, List


from ai_real_estate_deal_intelligence_machine.learning.historical_analyzer import (
    HistoricalAnalyzer,
)



class LearningMemory:
    """
    Persistent intelligence memory.

    Sprint 4 Part 7:

    Stores historical investment outcomes
    and extracts reusable knowledge.

    Flow:

    Deal Outcome
        |
        v
    Historical Memory
        |
        v
    Pattern Intelligence
    """



    def __init__(self):

        self.history: List[Dict[str, Any]] = []

        self.historical_analyzer = HistoricalAnalyzer()



    def store(
        self,
        deal_result: Dict[str, Any],
    ):
        """
        Store completed deal experience.
        """


        self.history.append(

            deal_result

        )



    def get_history(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return stored investment history.
        """


        return self.history



    def analyze_history(
        self,
    ) -> Dict[str, Any]:
        """
        Convert historical experience
        into investment intelligence.
        """


        return self.historical_analyzer.analyze(

            self.history

        )



    def get_learning_summary(
        self,
    ) -> Dict[str, Any]:
        """
        Provide current machine knowledge.
        """


        return {


            "total_deals":

                len(self.history),


            "historical_analysis":

                self.analyze_history(),


            "status":

                "MEMORY_ACTIVE",

        }