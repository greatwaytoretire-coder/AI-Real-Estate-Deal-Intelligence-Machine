from ai_real_estate_deal_intelligence_machine.acquisition.seller_outreach_engine import (
    SellerOutreachEngine,
)


def test_generate_seller_outreach():

    engine = SellerOutreachEngine()

    package = engine.generate(
        seller_id="SELLER-001",
        property_id="PROP-001",
        motivation_level="high",
        preferred_channel="phone",
    )

    assert package.seller_id == "SELLER-001"
    assert package.property_id == "PROP-001"
    assert package.outreach_channel == "phone"
    assert package.priority == "HIGH"
    assert package.status == "READY"
    assert "PROP-001" in package.message