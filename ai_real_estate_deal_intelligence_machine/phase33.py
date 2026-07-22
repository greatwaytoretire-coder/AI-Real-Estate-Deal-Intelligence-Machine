from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from .phase27 import ValidationStatus


@dataclass
class AIPrediction:
    """Stores the AI's predictions for a specific deal at a point in time."""

    prediction_id: str = field(default_factory=lambda: f"pred_{uuid4()}")
    deal_id: str = ""
    prediction_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    model_version: str = "1.0.0"
    data_source: str = "unknown"

    # Key Predictions
    deal_score: float = 0.0
    confidence: float = 0.0
    risk_score: float = 0.0
    estimated_purchase_price: float = 0.0
    estimated_arv: float = 0.0
    estimated_repairs: float = 0.0
    estimated_holding_costs: float = 0.0
    estimated_selling_costs: float = 0.0
    estimated_profit: float = 0.0
    estimated_roi: float = 0.0
    top_buyer_match_id: Optional[str] = None


@dataclass
class ActualOutcome:
    """Stores the real-world, verified outcome of a deal."""

    outcome_id: str = field(default_factory=lambda: f"out_{uuid4()}")
    deal_id: str = ""
    deal_outcome: str = "UNKNOWN"  # e.g., 'CLOSED', 'FAILED', 'PASSED'

    # Actual Financials
    actual_purchase_price: float = 0.0
    actual_repair_costs: float = 0.0
    actual_holding_costs: float = 0.0
    actual_selling_costs: float = 0.0
    actual_sale_price: float = 0.0

    # Performance Metrics
    days_to_sell: int = 0
    buyer_interest_level: float = 0.0  # e.g., number of inquiries or a scored value
    actual_buyer_id: Optional[str] = None

    @property
    def actual_roi(self) -> float:
        """Calculates the actual return on investment."""
        if self.actual_purchase_price == 0:
            return 0.0
        return (self.actual_profit / self.actual_purchase_price) * 100

    @property
    def actual_profit(self) -> float:
        """Calculates the actual profit from the outcome."""
        total_costs = (
            self.actual_purchase_price
            + self.actual_repair_costs
            + self.actual_holding_costs
            + self.actual_selling_costs
        )
        return self.actual_sale_price - total_costs


@dataclass
class ValidationResult:
    """Compares an AI prediction against an actual outcome to measure accuracy."""

    prediction: AIPrediction
    outcome: ActualOutcome

    @property
    def arv_variance_percent(self) -> float:
        if self.outcome.actual_sale_price == 0:
            return 0.0
        return (
            (self.prediction.estimated_arv - self.outcome.actual_sale_price)
            / self.outcome.actual_sale_price
        ) * 100

    @property
    def profit_variance_percent(self) -> float:
        if self.outcome.actual_profit == 0:
            return 0.0
        return (
            (self.prediction.estimated_profit - self.outcome.actual_profit)
            / self.outcome.actual_profit
        ) * 100

    def classify(self, field_name: str, tolerance_percent: float = 10.0) -> str:
        """Classifies a prediction field as Accurate, Overestimated, or Underestimated."""
        if field_name == "arv":
            variance = self.arv_variance_percent
        elif field_name == "profit":
            variance = self.profit_variance_percent
        else:
            return "Insufficient data"

        if abs(variance) <= tolerance_percent:
            return "Accurate"
        elif variance > 0:
            return "Overestimated"
        else:
            return "Underestimated"


@dataclass
class ValidationMetrics:
    """Aggregates validation metrics across a dataset of deals."""

    deals_validated: int = 0
    data_reliability: str = "No data"  # No data, Insufficient data, Preliminary, Reliable

    # Average Errors
    avg_arv_variance_percent: float = 0.0
    avg_profit_variance_percent: float = 0.0

    # Error Rates
    false_positive_rate: float = 0.0
    false_negative_rate: float = 0.0
    deal_conversion_rate: float = 0.0
    buyer_match_success_rate: float = 0.0


class ValidationManager:
    """Manages the storage, comparison, and validation of predictions vs. outcomes."""

    def __init__(self):
        self.predictions: Dict[str, AIPrediction] = {}
        self.outcomes: Dict[str, ActualOutcome] = {}
        self.learning_records: List[LearningRecord] = []

    def record_prediction(self, prediction: AIPrediction):
        """Stores an AI prediction for a given deal."""
        self.predictions[prediction.deal_id] = prediction

    def record_outcome(self, outcome: ActualOutcome):
        """Stores a verified real-world outcome for a given deal."""
        self.outcomes[outcome.deal_id] = outcome

    def generate_validation(self, deal_id: str) -> Optional[ValidationResult]:
        """Generates a comparison object if both prediction and outcome exist."""
        prediction = self.predictions.get(deal_id)
        outcome = self.outcomes.get(deal_id)

        if not prediction or not outcome:
            return None

        return ValidationResult(prediction=prediction, outcome=outcome)

    def create_learning_record(self, deal_id: str) -> Optional[LearningRecord]:
        """Creates a learning record from a completed validation."""
        validation = self.generate_validation(deal_id)
        if not validation:
            return None

        insight = f"ARV was {validation.classify('arv')}, Profit was {validation.classify('profit')}."

        record = LearningRecord(
            deal_id=deal_id,
            prediction_id=validation.prediction.prediction_id,
            outcome_id=validation.outcome.outcome_id,
            insight=insight,
            model_version=validation.prediction.model_version,
        )
        self.learning_records.append(record)
        return record

    def generate_metrics(
        self,
        deal_score_threshold: float = 80.0,
        profit_threshold: float = 10000.0,
        min_sample_size: int = 10,
    ) -> ValidationMetrics:
        """Generates aggregate validation metrics across all completed deals."""
        metrics = ValidationMetrics()
        validations = [self.generate_validation(deal_id) for deal_id in self.outcomes]
        completed_validations = [v for v in validations if v is not None]

        metrics.deals_validated = len(completed_validations)
        if metrics.deals_validated == 0:
            return metrics

        if metrics.deals_validated < min_sample_size:
            metrics.data_reliability = "Insufficient data"
        else:
            metrics.data_reliability = "Preliminary"

        total_arv_variance = 0
        total_profit_variance = 0
        false_positives = 0
        false_negatives = 0
        closed_deals = 0
        successful_matches = 0

        for v in completed_validations:
            total_arv_variance += v.arv_variance_percent
            total_profit_variance += v.profit_variance_percent

            # False positive: AI predicted a good deal, but it was bad.
            if v.prediction.deal_score >= deal_score_threshold and v.outcome.actual_profit < profit_threshold:
                false_positives += 1

            # False negative: AI predicted a bad deal, but it was good.
            if v.prediction.deal_score < deal_score_threshold and v.outcome.actual_profit >= profit_threshold:
                false_negatives += 1

            if v.outcome.deal_outcome == "CLOSED":
                closed_deals += 1
                # A match is successful if the predicted buyer is the one who actually closed the deal.
                if v.prediction.top_buyer_match_id and v.prediction.top_buyer_match_id == v.outcome.actual_buyer_id:
                    successful_matches += 1

        metrics.avg_arv_variance_percent = total_arv_variance / metrics.deals_validated
        metrics.avg_profit_variance_percent = total_profit_variance / metrics.deals_validated
        metrics.false_positive_rate = (false_positives / metrics.deals_validated) * 100
        metrics.false_negative_rate = (false_negatives / metrics.deals_validated) * 100
        metrics.deal_conversion_rate = (closed_deals / metrics.deals_validated) * 100
        if closed_deals > 0:
            metrics.buyer_match_success_rate = (successful_matches / closed_deals) * 100

        return metrics


@dataclass
class LearningRecord:
    """A record capturing a specific insight learned from a validation result."""

    learning_id: str = field(default_factory=lambda: f"learn_{uuid4()}")
    deal_id: str = ""
    prediction_id: str = ""
    outcome_id: str = ""
    insight: str = ""
    model_version: str = ""
    model_update_recommendation: str = ""
    created_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())