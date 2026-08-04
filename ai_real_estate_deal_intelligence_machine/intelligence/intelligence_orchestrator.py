from __future__ import annotations

from typing import Any, Dict

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)

from ai_real_estate_deal_intelligence_machine.intelligence.report_generator import (
    ReportGenerator,
)


class IntelligenceOrchestrator:
    """
    Coordinates the intelligence layer.

    Responsibilities:
    - Analyze opportunities
    - Generate recommendations
    - Create intelligence reports

    Future connections:
    - Acquisition AI Agent
    - Underwriting AI Agent
    - Machine Learning scoring
    - Live provider intelligence
    """

    def __init__(self):
        self.deal_analyzer = DealAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.report_generator = ReportGenerator()

    def analyze(
        self,
        opportunity: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute complete intelligence workflow.
        """

        analysis = self.deal_analyzer.analyze(
            opportunity
        )

        recommendation = self.recommendation_engine.generate(
            analysis
        )

        report = self.report_generator.generate(
            {
                "analysis": analysis,
                "recommendation": recommendation,
            }
        )

        return {
            "analysis": analysis,
            "recommendation": recommendation,
            "report": report,
        }