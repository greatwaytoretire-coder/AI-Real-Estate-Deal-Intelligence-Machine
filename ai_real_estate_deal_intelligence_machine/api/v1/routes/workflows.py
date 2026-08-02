from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.workflow import (
    DealIntelligenceRequest,
)

from ai_real_estate_deal_intelligence_machine.workflows.deal_intelligence_workflow import (
    DealIntelligenceWorkflow,
)


router = APIRouter(
    prefix="/workflows",
    tags=["workflows"],
)


workflow = DealIntelligenceWorkflow()


@router.post(
    "/intelligence"
)
def run_deal_intelligence(
    request: DealIntelligenceRequest,
):

    result = workflow.execute(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )


    return {

        "property_id":
            result.analysis.property_id,

        "analysis": {

            "mao":
                result.analysis.mao,

            "projected_profit":
                result.analysis.projected_profit,

            "profit_margin":
                result.analysis.profit_margin,

            "deal_score":
                result.analysis.deal_score,

            "investment_grade":
                result.analysis.investment_grade,
        },


        "report": {

            "summary":
                result.report.executive_summary,

            "recommended_action":
                result.report.recommended_action,

            "strengths":
                result.report.strengths,

            "risks":
                result.report.risks,
        },


        "recommendation":
            result.recommendation.recommendation,
    }