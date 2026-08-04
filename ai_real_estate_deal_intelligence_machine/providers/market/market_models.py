from dataclasses import dataclass


@dataclass
class MarketSnapshot:
    """
    Represents market intelligence data.
    """

    market: str
    median_price: float
    average_rent: float
    inventory_level: int
    days_on_market: int
    price_growth_rate: float
    rental_growth_rate: float
    investor_score: float
    source: str