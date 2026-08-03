from ai_real_estate_deal_intelligence_machine.acquisition.seller_lead_pipeline import (
    SellerLeadPipeline,
)


def test_seller_lead_pipeline_prioritizes_motivated_sellers():

    pipeline = SellerLeadPipeline()

    results = pipeline.prioritize_leads()

    assert len(results) > 0

    assert results[0].priority_score >= results[-1].priority_score

    assert results[0].recommendation in [
        "Immediate acquisition outreach.",
        "Priority follow-up.",
        "Nurture campaign.",
    ]

    assert len(results[0].reasoning) > 0