from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.investor_report import (
    InvestorReportRequest,
    InvestorReportResponse,
)

from ai_real_estate_deal_intelligence_machine.reports.investor_report_generator import (
    InvestorReportGenerator,
)


router = APIRouter(
    prefix="/investor-reports",
    tags=["Investor Reports"],
)


generator = InvestorReportGenerator()


@router.post(
    "",
    response_model=InvestorReportResponse,
)
def generate_investor_report(
    request: InvestorReportRequest,
):

    report = generator.generate(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )

    return InvestorReportResponse(
        property_id=report.property_id,
        executive_summary=(
            report.executive_summary
        ),
        recommendation=(
            report.recommendation
        ),
        deal_score=(
            report.deal_score
        ),
        projected_profit=(
            report.projected_profit
        ),
        profit_margin=(
            report.profit_margin
        ),
        risk_level=(
            report.risk_level
        ),
        status=(
            report.status
        ),
    )