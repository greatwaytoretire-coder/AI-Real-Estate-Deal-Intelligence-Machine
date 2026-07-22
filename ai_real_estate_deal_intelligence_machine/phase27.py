from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ValidationStatus(str, Enum):
    """Represents the outcome of a human review of an AI's analysis."""

    PENDING_REVIEW = "PENDING_REVIEW"
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
    PARTIALLY_CORRECT = "PARTIALLY_CORRECT"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass
class ValidatedDeal:
    """A record comparing AI analysis with human-reviewed validation."""

    deal_id: str
    # AI Predictions
    ai_estimated_arv: float
    ai_repair_estimate: float
    ai_deal_score: float
    ai_top_buyer_match: str  # buyer_id

    # Human Validation
    human_arv: float | None = None
    human_repair_estimate: float | None = None
    human_assessment: str | None = None  # Free-text assessment
    human_buyer_suitability: str | None = None  # Free-text assessment

    # Feedback
    feedback_status: ValidationStatus = ValidationStatus.PENDING_REVIEW
    feedback_notes: str | None = None


@dataclass
class AccuracyReport:
    """A report summarizing the accuracy of the AI's analysis against human validation."""

    opportunities_reviewed: int = 0
    underwriting_accuracy: float = 0.0  # % of deals where AI ARV/repairs are close to human
    buyer_matching_accuracy: float = 0.0  # Simple correct/incorrect for now
    false_positives: int = 0  # AI scored high, human scored low
    false_negatives: int = 0  # AI scored low, human scored high
    overvalued_properties: int = 0
    undervalued_properties: int = 0
    major_error_patterns: List[str] = field(default_factory=list)
    recommended_improvements: List[str] = field(default_factory=list)


class DealValidationEngine:
    """Manages the validation of AI deal analysis against human review."""

    def __init__(self, arv_tolerance: float = 0.05, repair_tolerance: float = 0.15):
        self.validation_dataset: List[ValidatedDeal] = []
        self.arv_tolerance = arv_tolerance
        self.repair_tolerance = repair_tolerance

    def submit_for_validation(self, deal: ValidatedDeal):
        """Adds a new AI-analyzed deal to the validation queue."""
        self.validation_dataset.append(deal)

    def record_feedback(self, deal_id: str, human_feedback: Dict[str, Any]):
        """Records a human operator's feedback for a specific deal."""
        deal = next((d for d in self.validation_dataset if d.deal_id == deal_id), None)
        if not deal:
            raise ValueError(f"Deal with ID {deal_id} not found in validation dataset.")

        deal.human_arv = human_feedback.get("human_arv")
        deal.human_repair_estimate = human_feedback.get("human_repair_estimate")
        deal.human_assessment = human_feedback.get("human_assessment")
        deal.human_buyer_suitability = human_feedback.get("human_buyer_suitability")
        deal.feedback_status = human_feedback.get("feedback_status", ValidationStatus.NEEDS_REVIEW)
        deal.feedback_notes = human_feedback.get("feedback_notes")

    def generate_accuracy_report(self) -> AccuracyReport:
        """Analyzes the validation dataset to produce an accuracy report."""
        report = AccuracyReport()
        validated_deals = [d for d in self.validation_dataset if d.feedback_status != ValidationStatus.PENDING_REVIEW]
        report.opportunities_reviewed = len(validated_deals)
        if not validated_deals:
            return report

        correct_underwriting = 0
        correct_matches = 0

        for deal in validated_deals:
            # Underwriting Accuracy
            arv_correct = abs(deal.ai_estimated_arv - deal.human_arv) / deal.human_arv <= self.arv_tolerance
            repair_correct = abs(deal.ai_repair_estimate - deal.human_repair_estimate) / deal.human_repair_estimate <= self.repair_tolerance
            if arv_correct and repair_correct:
                correct_underwriting += 1

            # Buyer Matching Accuracy (simple for now)
            if deal.feedback_status in [ValidationStatus.CORRECT, ValidationStatus.PARTIALLY_CORRECT]:
                correct_matches += 1

            # Error Patterns
            if deal.ai_deal_score > 80 and "bad" in (deal.human_assessment or "").lower():
                report.false_positives += 1
            if deal.ai_estimated_arv > deal.human_arv * (1 + self.arv_tolerance):
                report.overvalued_properties += 1
            if deal.ai_estimated_arv < deal.human_arv * (1 - self.arv_tolerance):
                report.undervalued_properties += 1

        report.underwriting_accuracy = (correct_underwriting / report.opportunities_reviewed) * 100
        report.buyer_matching_accuracy = (correct_matches / report.opportunities_reviewed) * 100

        if report.overvalued_properties > report.opportunities_reviewed / 2:
            report.major_error_patterns.append("System tends to overvalue properties.")
            report.recommended_improvements.append("Review ARV model for upward bias.")

        if report.false_positives > report.opportunities_reviewed / 3:
            report.major_error_patterns.append("Deal score produces a high number of false positives.")
            report.recommended_improvements.append("Incorporate human feedback into deal scoring model.")

        return report