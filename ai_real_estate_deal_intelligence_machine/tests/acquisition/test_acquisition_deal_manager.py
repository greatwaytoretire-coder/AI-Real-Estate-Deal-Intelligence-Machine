from ai_real_estate_deal_intelligence_machine.acquisition.deals.acquisition_deal_manager import (
    AcquisitionDealManager,
    AcquisitionDeal,
    AcquisitionDealStatus,
)



def test_get_acquisition_deals():

    manager = AcquisitionDealManager()


    deals = manager.get_deals()


    assert len(deals) == 1

    assert isinstance(
        deals[0],
        AcquisitionDeal,
    )


    assert deals[0].deal_id == "DEAL-001"

    assert deals[0].seller_id == "SELLER-001"

    assert deals[0].status == AcquisitionDealStatus.ANALYSIS_COMPLETE



def test_offer_readiness_score():

    manager = AcquisitionDealManager()


    deal = manager.get_deals()[0]


    score = manager.calculate_offer_readiness(
        deal
    )


    assert score >= 50



def test_advance_acquisition_deal_status():

    manager = AcquisitionDealManager()


    updated = manager.advance_status(
        deal_id="DEAL-001",
        new_status=AcquisitionDealStatus.OFFER_READY,
        note="Offer approved for seller review.",
    )


    assert updated.status == AcquisitionDealStatus.OFFER_READY


    assert (
        "Offer approved for seller review."
        in updated.notes
    )