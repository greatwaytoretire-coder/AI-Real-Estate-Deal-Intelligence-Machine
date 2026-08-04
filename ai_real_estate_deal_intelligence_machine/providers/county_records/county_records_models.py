from dataclasses import dataclass


@dataclass
class CountyPropertyRecord:
    """
    County property ownership and public record data model.
    """

    parcel_id: str
    owner_name: str
    property_address: str
    county: str
    state: str
    assessed_value: float
    year_built: int
    property_type: str
    last_sale_date: str
    last_sale_price: float
    tax_status: str