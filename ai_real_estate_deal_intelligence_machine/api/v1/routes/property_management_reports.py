from fastapi import APIRouter, HTTPException


from ai_real_estate_deal_intelligence_machine.api.schemas.property_management_reports import (
    PropertyManagementReportCreateRequest,
)


from ai_real_estate_deal_intelligence_machine.property_management_reports.property_management_reports_engine import (
    PropertyManagementReportsEngine,
)


router = APIRouter()


engine = PropertyManagementReportsEngine()



@router.post("")
def create_report(
    request: PropertyManagementReportCreateRequest
):

    try:

        report = engine.create_report(
            report_id=request.report_id,
            property_id=request.property_id,
            income=request.income,
            expenses=request.expenses,
            period=request.period,
        )

        return report


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )



@router.get("")
def get_reports():

    return engine.get_reports()