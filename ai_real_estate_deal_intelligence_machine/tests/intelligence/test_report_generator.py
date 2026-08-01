from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalysisResult,
)
from ai_real_estate_deal_intelligence_machine.intelligence.report_generator import (
    ReportGenerator,
)


def test_report_generation():

    analysis = DealAnalysisResult(
        property_id="PROP-001",
        mao=140000,
        projected_profit=65000,
        profit_margin=43.3,
        deal_score=90,
        investment_grade="STRONG",
    )

    report = ReportGenerator().generate(
        analysis,
    )

    assert report.property_id == "PROP-001"
    assert report.recommended_action == "PURSUE"
    assert len(report.strengths) >= 2