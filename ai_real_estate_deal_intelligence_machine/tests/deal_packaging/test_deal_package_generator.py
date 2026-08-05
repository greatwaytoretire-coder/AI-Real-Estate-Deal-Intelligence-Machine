from ai_real_estate_deal_intelligence_machine.deal_packaging.deal_package_generator import (
    DealPackageGenerator,
)


def test_package_contains_buyers():

    generator = DealPackageGenerator()

    package = generator.generate(
        underwriting={
            "property_id": "PROP-001",
            "address": "123 Main Street",
            "purchase_price": 200000,
            "arv": 300000,
            "projected_profit": 50000,
            "roi_percentage": 25.0,
            "recommendation": "BUY",
        },
        buyer_matches=[
            {"buyer_name": "Investor A"},
            {"buyer_name": "Investor B"},
        ],
    )

    assert len(package.buyer_recommendations) == 2


def test_summary_is_generated():

    generator = DealPackageGenerator()

    package = generator.generate(
        underwriting={
            "property_id": "PROP-001",
            "address": "123 Main Street",
            "purchase_price": 200000,
            "arv": 300000,
            "projected_profit": 50000,
            "roi_percentage": 25.0,
            "recommendation": "BUY",
        },
        buyer_matches=[],
    )

    assert package.summary != ""