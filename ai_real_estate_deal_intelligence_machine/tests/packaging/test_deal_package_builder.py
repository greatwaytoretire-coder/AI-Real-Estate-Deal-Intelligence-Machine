from ai_real_estate_deal_intelligence_machine.packaging.deal_package_builder import (
    DealPackageBuilder,
)


def test_build_deal_package():

    builder = DealPackageBuilder()

    package = builder.build(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    assert package.property_id == "PROP-001"

    assert package.status == "COMPLETED"

    assert package.deal_score > 0

    assert package.projected_profit > 0

    assert package.recommendation in [
        "ACQUIRE",
        "PURSUE",
        "NEGOTIATE",
        "PASS",
    ]