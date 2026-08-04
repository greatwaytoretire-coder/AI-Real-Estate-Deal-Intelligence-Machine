from enum import Enum


class ProviderCategory(str, Enum):
    """
    Categories of external intelligence providers.
    """

    PROPERTY = "property"
    MARKET = "market"
    BUYER = "buyer"
    SELLER = "seller"
    COUNTY_RECORDS = "county_records"
    MLS = "mls"
    FINANCIAL = "financial"


class ProviderStatus(str, Enum):
    """
    Provider availability state.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    MOCK = "mock"
    ERROR = "error"