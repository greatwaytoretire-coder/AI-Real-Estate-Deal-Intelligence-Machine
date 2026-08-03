from ai_real_estate_deal_intelligence_machine.acquisition.post_closing.asset_management_engine import (
    AssetManagementEngine,
    AssetStatus,
)


def test_create_asset():

    engine = AssetManagementEngine()

    asset = engine.create_asset(
        asset_id="ASSET-001",
        property_address="123 Main Street",
        acquisition_price=250000,
        closing_date="2026-08-03",
        strategy="Rental",
    )

    assert asset.asset_id == "ASSET-001"
    assert asset.property_address == "123 Main Street"
    assert asset.status == AssetStatus.ACQUIRED



def test_get_assets():

    engine = AssetManagementEngine()

    engine.create_asset(
        asset_id="ASSET-002",
        property_address="456 Oak Avenue",
        acquisition_price=300000,
        closing_date="2026-08-03",
        strategy="Flip",
    )

    assets = engine.get_assets()

    assert len(assets) == 1
    assert assets[0].asset_id == "ASSET-002"



def test_update_asset_status():

    engine = AssetManagementEngine()

    asset = engine.create_asset(
        asset_id="ASSET-003",
        property_address="789 Pine Road",
        acquisition_price=180000,
        closing_date="2026-08-03",
        strategy="Renovation",
    )

    updated = engine.update_status(
        asset_id=asset.asset_id,
        new_status=AssetStatus.RENOVATION,
        note="Renovation started.",
    )

    assert updated.status == AssetStatus.RENOVATION
    assert "Renovation started." in updated.notes



def test_income_and_expenses():

    engine = AssetManagementEngine()

    engine.create_asset(
        asset_id="ASSET-004",
        property_address="321 Elm Street",
        acquisition_price=220000,
        closing_date="2026-08-03",
        strategy="Rental",
    )

    engine.add_income(
        asset_id="ASSET-004",
        amount=2000,
    )

    engine.add_expense(
        asset_id="ASSET-004",
        amount=500,
    )

    performance = engine.calculate_performance(
        "ASSET-004"
    )

    assert performance["monthly_cash_flow"] == 1500



def test_missing_asset():

    engine = AssetManagementEngine()

    try:

        engine.update_status(
            asset_id="INVALID",
            new_status=AssetStatus.SOLD,
            note="Missing asset.",
        )

        assert False

    except ValueError as error:

        assert str(error) == "Asset not found."