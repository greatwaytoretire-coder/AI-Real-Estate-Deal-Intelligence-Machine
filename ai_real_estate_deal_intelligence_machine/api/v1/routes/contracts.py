from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.contract import (
    ContractCreate,
    ContractResponse,
)

from ai_real_estate_deal_intelligence_machine.acquisition.contracts.contract_management_engine import (
    ContractManagementEngine,
)


router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
)


contract_engine = ContractManagementEngine()



@router.post(
    "",
    response_model=ContractResponse,
)
def create_contract(
    contract: ContractCreate,
):

    created_contract = contract_engine.create_contract(
        contract_id=contract.contract_id,
        seller_id=contract.seller_id,
        property_address=contract.property_address,
        purchase_price=contract.purchase_price,
        earnest_money=contract.earnest_money,
    )

    return created_contract



@router.get(
    "",
    response_model=list[ContractResponse],
)
def get_contracts():

    return contract_engine.get_contracts()



@router.patch(
    "/{contract_id}/status",
    response_model=ContractResponse,
)
def update_contract_status(
    contract_id: str,
    status: str,
):

    try:

        from ai_real_estate_deal_intelligence_machine.acquisition.contracts.contract_management_engine import ContractStatus

        updated = contract_engine.update_status(
            contract_id=contract_id,
            new_status=ContractStatus(status),
            note="Status updated through API.",
        )

        return updated

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )