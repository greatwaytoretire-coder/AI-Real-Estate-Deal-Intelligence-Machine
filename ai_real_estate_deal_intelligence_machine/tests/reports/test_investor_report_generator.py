from ai_real_estate_deal_intelligence_machine.reports.investor_report_generator import (
    InvestorReportGenerator,
)


def test_generate_investor_report():

    generator = InvestorReportGenerator()

    report = generator.generate(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    assert report.property_id == "PROP-001"
    assert report.status == "COMPLETED"
    assert report.recommendation is not None
    assert report.executive_summary != ""
    assert report.deal_score > 0