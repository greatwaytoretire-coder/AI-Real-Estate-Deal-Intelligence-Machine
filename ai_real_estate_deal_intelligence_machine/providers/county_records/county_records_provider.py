from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.providers.base import (
    DataProvider,
    ProviderConfig,
)

from ai_real_estate_deal_intelligence_machine.providers.provider_types import (
    ProviderCategory,
)

from .county_records_models import CountyPropertyRecord


class CountyRecordsProvider(DataProvider):
    """
    County public records provider foundation.

    Future integrations:
    - ATTOM
    - CoreLogic
    - PropertyRadar
    - County assessor APIs
    - Recorder APIs
    """

    def __init__(self):
        self.record = self.get_config()

    def get_config(self) -> ProviderConfig:

        return ProviderConfig(
            name="county_records_provider",
            label="County Records Provider",
            source_type=ProviderCategory.COUNTY_RECORDS,
            api_key_env_var="COUNTY_RECORDS_API_KEY",
            cost_per_call=0.0,
        )

    def fetch(
        self,
        query: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        record = CountyPropertyRecord(
            parcel_id="PARCEL-001",
            owner_name="Mock Property Owner",
            property_address="100 County Records Lane",
            county="Maricopa",
            state="AZ",
            assessed_value=275000,
            year_built=1998,
            property_type="Single Family",
            last_sale_date="2022-05-15",
            last_sale_price=240000,
            tax_status="Current",
        )

        return [
            {
                "parcel_id": record.parcel_id,
                "owner_name": record.owner_name,
                "property_address": record.property_address,
                "county": record.county,
                "state": record.state,
                "assessed_value": record.assessed_value,
                "year_built": record.year_built,
                "property_type": record.property_type,
                "last_sale_date": record.last_sale_date,
                "last_sale_price": record.last_sale_price,
                "tax_status": record.tax_status,
            }
        ]