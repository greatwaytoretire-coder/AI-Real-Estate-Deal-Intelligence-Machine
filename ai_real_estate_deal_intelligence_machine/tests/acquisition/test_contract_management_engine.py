from ai_real_estate_deal_intelligence_machine.acquisition.contracts.contract_management_engine import (
    ContractManagementEngine,
    ContractStatus,
)


def test_create_contract():

    engine = ContractManagementEngine()

    contract = engine.create_contract(
        contract_id="CONTRACT-001",
        seller_id="SELLER-001",
        property_address="123 Main Street",
        purchase_price=150000,
        earnest_money=5000,
    )

    assert contract.contract_id == "CONTRACT-001"
    assert contract.seller_id == "SELLER-001"
    assert contract.purchase_price == 150000
    assert contract.status == ContractStatus.DRAFT



def test_get_contracts():

    engine = ContractManagementEngine()

    engine.create_contract(
        contract_id="CONTRACT-002",
        seller_id="SELLER-002",
        property_address="456 Oak Avenue",
        purchase_price=200000,
        earnest_money=10000,
    )

    contracts = engine.get_contracts()

    contract_ids = [
        contract.contract_id
        for contract in contracts
    ]

    assert "CONTRACT-002" in contract_ids



def test_update_contract_status():

    engine = ContractManagementEngine()

    engine.create_contract(
        contract_id="CONTRACT-003",
        seller_id="SELLER-003",
        property_address="789 Pine Road",
        purchase_price=175000,
        earnest_money=7500,
    )

    updated = engine.update_status(
        contract_id="CONTRACT-003",
        new_status=ContractStatus.SIGNED,
        note="Seller signed purchase agreement.",
    )

    assert updated.status == ContractStatus.SIGNED
    assert "Seller signed purchase agreement." in updated.notes



def test_contract_progression():

    engine = ContractManagementEngine()

    contract = engine.create_contract(
        contract_id="CONTRACT-004",
        seller_id="SELLER-004",
        property_address="321 Elm Street",
        purchase_price=225000,
        earnest_money=12000,
    )

    updated = engine.update_status(
        contract_id=contract.contract_id,
        new_status=ContractStatus.SIGNED,
        note="Title review completed.",
    )

    assert updated.status == ContractStatus.SIGNED



def test_missing_contract():

    engine = ContractManagementEngine()

    try:

        engine.update_status(
            contract_id="INVALID",
            new_status=ContractStatus.SIGNED,
            note="Invalid contract.",
        )

        assert False

    except ValueError as error:

        assert str(error) == "Contract not found."