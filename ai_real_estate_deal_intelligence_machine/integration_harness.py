from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .audit_logger import AuditLogger
from .db_client import DatabaseClient
from .phase3 import HeatMapEngine, MarketAlertSystem, MarketIntelligenceAgent
from .phase4 import PropertyDiscoveryAgent
from .phase6 import ARVAgent, ComparableSalesAgent, RepairEstimationAgent
from .phase7 import DealUnderwritingAgent
from .phase5 import OpportunityScoringEngine, PriorityDealQueue
from .phase9 import BuyerIntelligenceEngine
from .phase10 import BuyerMatchingEngine
from .phase11 import SellerAcquisitionAgent, SellerOpportunity, SellerStage
from .phase12 import BuyerDispositionAgent
from .phase13 import DealRoomAgent
from .phase14 import DealLifecycleWorkflow, NextBestActionEngine
from .phase15 import OutcomeLearningEngine


@dataclass
class IntegrationStageResult:
    status: str
    output: Dict[str, Any]
    error: Optional[str] = None


class EndToEndIntegrationHarness:
    def __init__(self, db_path: Optional[Path] = None, audit_log_path: Optional[Path] = None, simulate_failure: Optional[str] = None) -> None:
        self.db_client = DatabaseClient(database_path=db_path or Path("data/phase22.db"))
        self.audit_logger = AuditLogger(log_path=audit_log_path or Path("data/phase22-audit.log"))
        self.simulate_failure = simulate_failure
        self._stage_results: Dict[str, IntegrationStageResult] = {}

    def _serialize_payload(self, value: Any) -> Any:
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(key): self._serialize_payload(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._serialize_payload(item) for item in value]
        if is_dataclass(value):
            return self._serialize_payload(asdict(value))
        if hasattr(value, "as_dict") and callable(value.as_dict):
            return self._serialize_payload(value.as_dict())
        if hasattr(value, "__dict__"):
            return self._serialize_payload(vars(value))
        return str(value)

    def _record_stage(self, stage: str, result: IntegrationStageResult) -> None:
        self._stage_results[stage] = result
        payload = {"status": result.status, "output": self._serialize_payload(result.output), "error": result.error}
        self.db_client.record_stage_result(stage, payload)
        self.db_client.log_audit("integration_stage", f"{stage}:{result.status}:{result.error or 'ok'}")
        self.audit_logger.log("integration_stage", f"{stage}:{result.status}")

    def _safe_stage(self, stage: str, func: Any) -> IntegrationStageResult:
        try:
            if self.simulate_failure and stage == self.simulate_failure:
                raise RuntimeError(f"simulated failure in {stage}")
            output = func()
            return IntegrationStageResult(status="ok", output=output)
        except Exception as exc:  # pragma: no cover - defensive path
            return IntegrationStageResult(status="error", output={}, error=str(exc))

    def run(self) -> Dict[str, Any]:
        stages: Dict[str, Any] = {}
        data_flow: Dict[str, bool] = {
            "market_to_property": False,
            "property_to_underwriting": False,
            "underwriting_to_score": False,
            "score_to_buyer_match": False,
            "buyer_match_to_package": False,
            "package_to_workflow": False,
            "workflow_to_outcome": False,
            "outcome_to_learning": False,
        }
        errors: List[str] = []

        market = self._safe_stage("market_intelligence", lambda: MarketIntelligenceAgent().rank_markets())
        self._record_stage("market_intelligence", market)
        stages["market_intelligence"] = {
            "status": market.status,
            "source_label": "mock-market-feed",
            "output": market.output,
        }

        property_stage = self._safe_stage("property_discovery", lambda: PropertyDiscoveryAgent().find_deal_candidates())
        self._record_stage("property_discovery", property_stage)
        stages["property_discovery"] = {
            "status": property_stage.status,
            "source_label": "mock-property-feed",
            "output": property_stage.output,
        }

        property_intelligence = self._safe_stage("property_intelligence", lambda: {
            "property_count": len(property_stage.output),
            "candidate_addresses": [item.property_profile.address for item in property_stage.output] if property_stage.status == "ok" else [],
        })
        self._record_stage("property_intelligence", property_intelligence)
        stages["property_intelligence"] = {
            "status": property_intelligence.status,
            "source_label": "mock-property-feed",
            "output": property_intelligence.output,
        }

        seller_signal = self._safe_stage("seller_signal_detection", lambda: SellerAcquisitionAgent().identify_high_priority_opportunity())
        self._record_stage("seller_signal_detection", seller_signal)
        stages["seller_signal_detection"] = {
            "status": seller_signal.status,
            "source_label": "mock-seller-feed",
            "output": self._serialize_payload(seller_signal.output) if seller_signal.status == "ok" else {},
        }

        comps = self._safe_stage("comparable_sales", lambda: ComparableSalesAgent().identify_comparables())
        self._record_stage("comparable_sales", comps)
        stages["comparable_sales"] = {
            "status": comps.status,
            "source_label": "mock-comparable-feed",
            "output": comps.output,
        }

        underwriting = self._safe_stage("underwriting", lambda: DealUnderwritingAgent().generate_event().payload)
        self._record_stage("underwriting", underwriting)
        stages["underwriting"] = {
            "status": underwriting.status,
            "source_label": "mock-underwriting-feed",
            "output": underwriting.output,
        }

        deal_score = self._safe_stage("deal_scoring", lambda: OpportunityScoringEngine().promote_high_scoring(PriorityDealQueue()))
        self._record_stage("deal_scoring", deal_score)
        stages["deal_scoring"] = {
            "status": deal_score.status,
            "source_label": "mock-score-feed",
            "output": deal_score.output,
        }

        buyer_intelligence = self._safe_stage("buyer_intelligence", lambda: BuyerIntelligenceEngine().generate_event().payload)
        self._record_stage("buyer_intelligence", buyer_intelligence)
        stages["buyer_intelligence"] = {
            "status": buyer_intelligence.status,
            "source_label": "mock-buyer-feed",
            "output": buyer_intelligence.output,
        }

        buyer_match = self._safe_stage("buyer_matching", lambda: BuyerMatchingEngine().rank_buyers())
        self._record_stage("buyer_matching", buyer_match)
        stages["buyer_matching"] = {
            "status": buyer_match.status,
            "source_label": "mock-buyer-feed",
            "output": buyer_match.output,
        }

        deal_package = self._safe_stage("deal_packaging", lambda: {
            "deal_room": DealRoomAgent().generate_deal_room().deal_id,
            "underwriting": underwriting.output if underwriting.status == "ok" else {},
            "buyer_matches": buyer_match.output if buyer_match.status == "ok" else {},
        })
        self._record_stage("deal_packaging", deal_package)
        stages["deal_packaging"] = {
            "status": deal_package.status,
            "source_label": "mock-deal-room",
            "output": deal_package.output,
        }

        acquisition = self._safe_stage("acquisition_workflow", lambda: {
            "seller": self._serialize_payload(seller_signal.output) if seller_signal.status == "ok" else {},
            "qualification": self._serialize_payload(SellerAcquisitionAgent().build_qualification_plan(seller_signal.output)) if seller_signal.status == "ok" else {},
        })
        self._record_stage("acquisition_workflow", acquisition)
        stages["acquisition_workflow"] = {
            "status": acquisition.status,
            "source_label": "mock-acquisition-workflow",
            "output": acquisition.output,
        }

        disposition = self._safe_stage("disposition_workflow", lambda: BuyerDispositionAgent().generate_deal_summary().as_dict())
        self._record_stage("disposition_workflow", disposition)
        stages["disposition_workflow"] = {
            "status": disposition.status,
            "source_label": "mock-disposition-workflow",
            "output": disposition.output,
        }

        outcome = self._safe_stage("outcome_tracking", lambda: {
            "workflow": DealLifecycleWorkflow().as_dict(),
            "next_actions": NextBestActionEngine().recommend_next_actions(DealLifecycleWorkflow()),
        })
        self._record_stage("outcome_tracking", outcome)
        stages["outcome_tracking"] = {
            "status": outcome.status,
            "source_label": "mock-outcome-workflow",
            "output": outcome.output,
        }

        learning = self._safe_stage("learning_system", lambda: OutcomeLearningEngine().create_learning_version().version)
        self._record_stage("learning_system", learning)
        stages["learning_system"] = {
            "status": learning.status,
            "source_label": "mock-learning-system",
            "output": learning.output,
        }

        if market.status == "ok" and property_stage.status == "ok":
            data_flow["market_to_property"] = True
        if property_stage.status == "ok" and underwriting.status == "ok":
            data_flow["property_to_underwriting"] = True
        if underwriting.status == "ok" and deal_score.status == "ok":
            data_flow["underwriting_to_score"] = True
        if deal_score.status == "ok" and buyer_match.status == "ok":
            data_flow["score_to_buyer_match"] = True
        if buyer_match.status == "ok" and deal_package.status == "ok":
            data_flow["buyer_match_to_package"] = True
        if deal_package.status == "ok" and acquisition.status == "ok":
            data_flow["package_to_workflow"] = True
        if acquisition.status == "ok" and outcome.status == "ok":
            data_flow["workflow_to_outcome"] = True
        if outcome.status == "ok" and learning.status == "ok":
            data_flow["outcome_to_learning"] = True

        for stage_name, result in self._stage_results.items():
            if result.status == "error":
                errors.append(stage_name)

        trace = {
            "status": "ok" if not errors else "degraded",
            "stages": stages,
            "data_flow": data_flow,
            "errors": errors,
            "stage_results": {name: {"status": result.status, "error": result.error} for name, result in self._stage_results.items()},
            "audit_logs": self.db_client.list_audit_logs(),
            "stage_records": self.db_client.list_stage_results(),
        }
        self.db_client.close()
        return trace
