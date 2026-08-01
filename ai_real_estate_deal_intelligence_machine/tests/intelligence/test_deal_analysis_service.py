from ai_real_estate_deal_intelligence_machine.services.deal_analysis_service import (
    DealAnalysisService,
)


def test_complete_deal_analysis_pipeline():

    service = DealAnalysisService()

    result = service.analyze(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    assert result.analysis.projected_profit == 65000

    assert result.analysis.investment_grade == "STRONG"

    assert result.report.recommended_action == "PURSUE"