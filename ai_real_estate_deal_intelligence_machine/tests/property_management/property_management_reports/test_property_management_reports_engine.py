from ai_real_estate_deal_intelligence_machine.property_management_reports.property_management_reports_engine import (
    PropertyManagementReportsEngine,
)



def test_create_report():

    engine = PropertyManagementReportsEngine()


    report = engine.create_report(
        report_id="REPORT-001",
        property_id="PROP-001",
        income=5000,
        expenses=2000,
        period="2026-08",
    )


    assert report["report_id"] == "REPORT-001"
    assert report["noi"] == 3000



def test_get_reports():

    engine = PropertyManagementReportsEngine()


    engine.create_report(
        report_id="REPORT-002",
        property_id="PROP-002",
        income=6000,
        expenses=2500,
        period="2026-08",
    )


    reports = engine.get_reports()


    assert len(reports) == 1