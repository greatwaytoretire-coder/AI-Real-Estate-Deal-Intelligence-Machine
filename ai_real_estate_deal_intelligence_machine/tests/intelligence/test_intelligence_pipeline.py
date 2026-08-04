from ai_real_estate_deal_intelligence_machine.intelligence.intelligence_pipeline import (
    IntelligencePipeline,
)


def test_pipeline():

    pipeline = IntelligencePipeline()

    packet = pipeline.process()

    assert packet.property_data["address"] == "500 Intelligence Avenue"
    assert packet.market_data["market_score"] == 91
    assert packet.valuation_data["estimated_value"] == 338000
    assert packet.confidence_score == 0.90