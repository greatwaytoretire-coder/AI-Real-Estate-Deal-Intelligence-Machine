from ai_real_estate_deal_intelligence_machine.disposition.buyer_outreach_engine import (
    BuyerOutreachEngine,
)


def test_generate_buyer_outreach():

    engine = BuyerOutreachEngine()


    package = engine.generate(
        property_id="PROP-001",
        buyer_id="BUYER-001",
        buyer_type="cash_investor",
        preferred_channel="email",
    )


    assert package.property_id == "PROP-001"

    assert package.buyer_id == "BUYER-001"

    assert package.outreach_channel == "email"

    assert package.priority == "HIGH"

    assert package.status == "READY"

    assert "PROP-001" in package.message