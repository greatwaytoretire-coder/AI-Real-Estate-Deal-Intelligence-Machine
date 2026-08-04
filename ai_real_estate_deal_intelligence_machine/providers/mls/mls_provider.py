from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.providers.base import (
    DataProvider,
    ProviderConfig,
)

from ai_real_estate_deal_intelligence_machine.providers.provider_types import (
    ProviderCategory,
)

from .mls_models import MLSListing


class MLSProvider(DataProvider):
    """
    MLS data provider abstraction.

    Future integrations:
    - RESO Web API
    - MLS Grid
    - Spark API
    - Regional MLS feeds
    """

    def __init__(self):
        self.record = self.get_config()

    def get_config(self) -> ProviderConfig:

        return ProviderConfig(
            name="mls_provider",
            label="MLS Listing Provider",
            source_type=ProviderCategory.MLS,
            api_key_env_var="MLS_API_KEY",
            cost_per_call=0.0,
        )

    def fetch(
        self,
        query: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Temporary mock MLS response.

        Production MLS APIs will replace this layer.
        """

        listing = MLSListing(
            listing_id="MLS-001",
            address="500 Intelligence Avenue",
            city="Phoenix",
            state="AZ",
            zip_code="85001",
            price=325000,
            bedrooms=3,
            bathrooms=2,
            square_feet=1650,
            property_type="Single Family",
            status="Active",
            days_on_market=12,
            listing_source="Mock MLS",
        )

        return [
            {
                "listing_id": listing.listing_id,
                "address": listing.address,
                "city": listing.city,
                "state": listing.state,
                "zip_code": listing.zip_code,
                "price": listing.price,
                "bedrooms": listing.bedrooms,
                "bathrooms": listing.bathrooms,
                "square_feet": listing.square_feet,
                "property_type": listing.property_type,
                "status": listing.status,
                "days_on_market": listing.days_on_market,
                "listing_source": listing.listing_source,
            }
        ]