from dataclasses import dataclass


@dataclass
class PropertyValuation:
    """
    Property valuation intelligence model.
    """

    property_id: str
    address: str
    estimated_value: float
    confidence_score: float
    rental_estimate: float
    comparable_count: int
    valuation_source: str