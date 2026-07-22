from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from .phase25 import ActionForApproval, HumanInTheLoopEngine
from .phase33 import ValidationManager, ValidationMetrics


class ModelVersionStatus(str, Enum):
    """Lifecycle status of a model version."""

    PROPOSED = "PROPOSED"
    EVALUATING = "EVALUATING"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    REJECTED = "REJECTED"


@dataclass
class ModelVersion:
    """Tracks a specific version of a scoring model or learning change."""

    version_id: str = field(default_factory=lambda: f"mv_{uuid4()}")
    model_name: str = ""
    status: ModelVersionStatus = ModelVersionStatus.PROPOSED
    changes: str = ""
    based_on_version_id: Optional[str] = None

    # Metadata
    data_used: List[str] = field(default_factory=list)  # e.g., list of deal_ids
    metrics: Optional[ValidationMetrics] = None
    approval_action_id: Optional[str] = None
    deployment_date: Optional[str] = None
    created_date: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class ModelImprovementProposal:
    """A candidate improvement proposal for a model, generated from error analysis."""

    target_model: str  # e.g., 'ARV_ESTIMATION'
    recommendation: str
    supporting_deal_id: str
    error_analysis: str


class ModelRegistry:
    """Manages the lifecycle of model versions, including deployment and rollback."""

    def __init__(self):
        self.versions: Dict[str, ModelVersion] = {}

    def propose_new_version(self, proposal: ModelImprovementProposal) -> ModelVersion:
        """Creates a new model version from a proposal."""
        active_version = self.get_active_version(proposal.target_model)
        new_version = ModelVersion(
            model_name=proposal.target_model,
            changes=proposal.recommendation,
            data_used=[proposal.supporting_deal_id],
            based_on_version_id=active_version.version_id if active_version else None,
        )
        self.versions[new_version.version_id] = new_version
        return new_version

    def get_active_version(self, model_name: str) -> Optional[ModelVersion]:
        """Finds the currently active version for a given model."""
        for version in self.versions.values():
            if version.model_name == model_name and version.status == ModelVersionStatus.ACTIVE:
                return version
        return None

    def deploy_version(self, version_id: str) -> bool:
        """Activates a new version and archives the old one."""
        new_version = self.versions.get(version_id)
        if not new_version or new_version.status != ModelVersionStatus.EVALUATING:
            return False

        # Archive the currently active version
        active_version = self.get_active_version(new_version.model_name)
        if active_version:
            active_version.status = ModelVersionStatus.ARCHIVED

        # Deploy the new version
        new_version.status = ModelVersionStatus.ACTIVE
        new_version.deployment_date = datetime.utcnow().isoformat()
        return True

    def rollback_to_version(self, version_id: str) -> bool:
        """Rolls back to a previously archived version."""
        version_to_restore = self.versions.get(version_id)
        if not version_to_restore or version_to_restore.status != ModelVersionStatus.ARCHIVED:
            return False
        # This is a simplified deployment; a real one would have more checks.
        version_to_restore.status = ModelVersionStatus.EVALUATING # Set to eval before deploy
        return self.deploy_version(version_id)


class LearningPipelineOrchestrator:
    """
    Phase 38: Orchestrates the controlled learning pipeline, turning validation
    results into actionable, human-approved model improvement proposals.
    """

    def __init__(self, validation_manager: ValidationManager, hitl_engine: HumanInTheLoopEngine):
        self.validation_manager = validation_manager
        self.hitl_engine = hitl_engine

    def run_for_deal(self, deal_id: str) -> Optional[ModelImprovementProposal]:
        """Analyzes a deal's outcome and proposes improvements if necessary."""
        validation = self.validation_manager.generate_validation(deal_id)
        if not validation:
            return None

        # Error Analysis
        if abs(validation.arv_variance_percent) > 15.0:  # If ARV estimate was off by > 15%
            proposal = ModelImprovementProposal(
                target_model="ARV_ESTIMATION",
                recommendation="Recalibrate ARV model weights for this market segment.",
                supporting_deal_id=deal_id,
                error_analysis=f"ARV was {validation.classify('arv')} by {validation.arv_variance_percent:.2f}%.",
            )

            # Create an action for human approval
            action = ActionForApproval(
                action_type="MODEL_UPDATE_PROPOSAL",
                recommendation=f"Approve evaluation of new ARV model weights based on outcome of deal {deal_id}.",
                reasoning=proposal.error_analysis,
                action_payload=proposal.__dict__,
            )
            self.hitl_engine.submit_for_approval(action)
            return proposal

        return None