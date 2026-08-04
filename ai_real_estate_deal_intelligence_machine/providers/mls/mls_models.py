from dataclasses import dataclass
from typing import Optional


@dataclass
class MLSListing:
    """
    Standardized MLS property listing model.

    This model allows different MLS providers
    to map into one common format.
    """

    listing_id: str
    address: str
    city: str
    state: str
    zip_code: str

    price: float

    bedrooms: int
    bathrooms: float

    square_feet: int

    property_type: str

    status: str

    days_on_market: int

    listing_source: Optional[str] = None