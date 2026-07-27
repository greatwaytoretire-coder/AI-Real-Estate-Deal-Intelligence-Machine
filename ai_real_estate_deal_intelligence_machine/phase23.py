from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .audit_logger import AuditLogger
from .phase3 import MarketIntelligenceAgent
from .phase4 import PropertyDiscoveryAgent
from .phase5 import OpportunityScoringEngine, ScoringInput
from .phase6 import ARVAgent, ComparableSalesAgent, RepairEstimationAgent
from .phase7 import DealUnderwritingAgent
from .phase8 import DealRiskAgent, DealRiskAgentInput
from .phase9 import BuyerIntelligenceEngine
from .phase10 import BuyerMatchingEngine
from .phase11 import SellerAcquisitionAgent
from .phase14 import DealLifecycleWorkflow, NextBestActionEngine
from .phase15 import OutcomeLearningEngine
from .phase16 import MissionControlMetrics


@dataclass
class EndToEndSimulationReport:
    """Report from a single end-to-end simulation run."""

    stages_completed: List[str] = field(default_factory=list)
    stages_failed: Dict[str, str] = field(default_factory=dict)
    stage_data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    final_deal_score: float | None = None
    final_risk_score: float | None = None
    final_buyer_match_score: float | None = None
    final_deal_package: Dict[str, Any] | None = None

    reproducible: bool = True


class EndToEndDealSimulation:
    """Phase 23: Complete end-to-end simulation using mock data."""

    def run(self) -> EndToEndSimulationReport:
        """Execute the complete end-to-end simulation."""

        report = EndToEndSimulationReport()
        context: Dict[str, Any] = {}

        def run_stage(
            stage_name: str,
            func,
            *args,
            record_completion: bool = True,
            **kwargs,
        ):
            try:
                result = func(*args, **kwargs)

                if record_completion:
                    report.stages_completed.append(stage_name)
                report.stage_data[stage_name] = result

                return result

            except Exception as exc:
                error_message = (
                    f"Stage '{stage_name}' failed: {exc}"
                )

                report.stages_failed[stage_name] = error_message
                report.errors.append(error_message)

                return None

        # ==========================================================
        # 1. MARKET INTELLIGENCE
        # ==========================================================

        market_agent = MarketIntelligenceAgent()

        market_summary = run_stage(
            "Market Intelligence",
            market_agent.rank_markets,
        )

        if not market_summary:
            return report

        context["market_summary"] = market_summary

        # ==========================================================
        # 2. PROPERTY DISCOVERY
        # ==========================================================

        property_agent = PropertyDiscoveryAgent()

        deal_candidates = run_stage(
            "Property Discovery",
            property_agent.find_deal_candidates,
        )

        if not deal_candidates:
            return report

        property_profile = deal_candidates[0].property_profile

        context["deal_candidates"] = deal_candidates
        context["property_profile"] = property_profile

        # ==========================================================
        # 3. SELLER MOTIVATION
        # ==========================================================

        seller_agent = SellerAcquisitionAgent()

        seller_opportunity = run_stage(
            "Seller Motivation",
            seller_agent.identify_high_priority_opportunity,
        )

        if not seller_opportunity:
            return report

        context["seller_opportunity"] = seller_opportunity

        # ==========================================================
        # 4. COMPARABLE SALES
        # ==========================================================

        comps_agent = ComparableSalesAgent()

        comp_set = run_stage(
            "Comparable Sales",
            comps_agent.identify_comparables,
        )

        if not comp_set:
            return report

        context["comp_set"] = comp_set

        # ==========================================================
        # 5. ARV CALCULATION
        # ==========================================================

        arv_agent = ARVAgent()

        arv_estimate = run_stage(
            "ARV Calculation",
            arv_agent.estimate_arv,
        )

        if not arv_estimate:
            return report

        context["arv_estimate"] = arv_estimate

        # ==========================================================
        # 6. REPAIR ESTIMATION
        # ==========================================================

        repair_agent = RepairEstimationAgent()

        repair_estimate = run_stage(
            "Repair Estimation",
            repair_agent.estimate_repairs,
        )

        if not repair_estimate:
            return report

        context["repair_estimate"] = repair_estimate

        # ==========================================================
        # 7. UNDERWRITING
        # ==========================================================

        underwriting_agent = DealUnderwritingAgent()

        underwriting_result = run_stage(
            "Underwriting",
            lambda: underwriting_agent.generate_event().payload,
        )

        if not underwriting_result:
            return report

        context["underwriting_result"] = underwriting_result

        # ==========================================================
        # 8. DEAL SCORING
        # ==========================================================

        scoring_engine = OpportunityScoringEngine(
            audit_logger=AuditLogger()
        )

        scoring_input = ScoringInput(
            correlation_id="sim-run",
            market_id=context["market_summary"][0]["market"],
        )

        deal_scorecard = run_stage(
            "Deal Scoring",
            lambda: scoring_engine.execute(
                scoring_input
            ).scorecard,
        )

        if not deal_scorecard:
            return report

        context["deal_scorecard"] = deal_scorecard

        report.final_deal_score = (
            deal_scorecard.deal_potential_score
        )

        # ==========================================================
        # 9. RISK SCORING
        # ==========================================================

        risk_agent = DealRiskAgent(
            audit_logger=AuditLogger()
        )

        risk_input = DealRiskAgentInput(
            correlation_id="sim-run",
            deal_id="sim-deal-01",
        )

        risk_assessment = run_stage(
            "Risk Scoring",
            lambda: risk_agent.execute(
                risk_input
            ).assessment,
        )

        if not risk_assessment:
            return report

        context["risk_assessment"] = risk_assessment

        report.final_risk_score = (
            risk_assessment.risk_score
        )

        # ==========================================================
        # 10. BUYER DISCOVERY
        # ==========================================================

        buyer_engine = BuyerIntelligenceEngine()

        buyer_events = run_stage(
            "Buyer Discovery",
            lambda: [
                buyer_engine.generate_event("buyer-0001"),
                buyer_engine.generate_event("buyer-0002"),
            ],
        )

        if not buyer_events:
            return report

        context["buyer_events"] = buyer_events

        # ==========================================================
        # 11. PHASE 9 -> PHASE 10 ADAPTER
        # ==========================================================

        adapted_buyer_database: List[Dict[str, Any]] = []

        for event in buyer_events:

            payload = event.payload

            buyer_data = payload["buyer"]
            activity_data = payload["activity"]
            reliability_data = payload["reliability"]

            purchase_range = buyer_data["purchase_range"]

            price_range = (
                f"{int(purchase_range[0])}-"
                f"{int(purchase_range[1])}"
            )

            adapted_buyer_database.append(
                {
                    "buyer_id": buyer_data["buyer_id"],
                    "location": buyer_data["geography"],
                    "price": price_range,
                    "property_type": buyer_data["property_type"],
                    "strategy": buyer_data["strategy"],

                    # These fields are not supplied by Phase 9.
                    # No data is fabricated.
                    "repair_profile": None,
                    "arv": None,
                    "historical_behavior": None,

                    "verified": reliability_data["verified"],
                    "reliability_score": (
                        reliability_data["reliability_score"]
                    ),
                    "recent_activity": (
                        activity_data["recent_activity"]
                    ),
                    "transaction_activity": (
                        activity_data["transaction_activity"]
                    ),
                    "proof_of_funds": (
                        buyer_data["proof_of_funds"]
                    ),
                }
            )

        context["adapted_buyer_database"] = (
            adapted_buyer_database
        )

        # ==========================================================
        # 12. BUYER MATCHING
        # ==========================================================

        buyer_matching_engine = BuyerMatchingEngine(
            buyer_database=adapted_buyer_database
        )

        buyer_matches = run_stage(
            "Buyer Matching",
            buyer_matching_engine.rank_buyers,
        )

        if not buyer_matches:
            return report

        context["buyer_matches"] = buyer_matches

        top_matches = buyer_matches.get(
            "TOP 10 BUYER MATCHES",
            [],
        )

        if top_matches:

            report.final_buyer_match_score = (
                top_matches[0].get("score")
            )

        # ==========================================================
        # 13. DEAL ROOM PACKAGE
        # ==========================================================
        #
        # The current repository does not contain a DealRoomAgent
        # or DealRoomMetrics implementation.
        #
        # Therefore, Phase 23 creates a transparent simulation
        # package directly from data already produced by earlier
        # stages instead of calling a nonexistent component.

        deal_package = run_stage(
            "Deal Packaging",
            lambda: {
                "deal_room_id": "sim-deal-room-001",
                "status": (
                    "Investor-Ready Package (SIMULATION)"
                ),
                "property_address": (
                    getattr(
                        property_profile,
                        "address",
                        None,
                    )
                ),
                "arv": (
                    getattr(
                        arv_estimate,
                        "arv",
                        None,
                    )
                    if arv_estimate
                    else None
                ),
                "estimated_profit": (
                    underwriting_result.get(
                        "estimated_profit"
                    )
                ),
                "deal_score": (
                    report.final_deal_score
                ),
                "risk_score": (
                    report.final_risk_score
                ),
                "top_buyer_matches": top_matches,
            },
        )

        if not deal_package:
            return report

        context["deal_package"] = deal_package
        report.final_deal_package = deal_package

        # ==========================================================
        # 14. WORKFLOW PREPARATION
        # ==========================================================

        lifecycle_workflow = run_stage(
            "Workflow Preparation",
            DealLifecycleWorkflow,
        )

        if not lifecycle_workflow:
            return report

        context["lifecycle_workflow"] = (
            lifecycle_workflow
        )

        # ==========================================================
        # 15. NEXT BEST ACTION
        # ==========================================================

        next_action_engine = NextBestActionEngine()

        next_actions = run_stage(
            "Next Best Action",
            next_action_engine.recommend_next_actions,
            lifecycle_workflow,
            record_completion=False,
        )

        if not next_actions:
            return report

        context["next_actions"] = next_actions

        # ==========================================================
        # 16. SIMULATED OUTCOME RECORDING
        # ==========================================================

        simulated_outcome = run_stage(
            "Outcome Recording",
            lambda: {
                "outcome": "CLOSED_DEAL",
                "final_price": 400000,
                "notes": (
                    "Simulated successful closing."
                ),
            },
        )

        if not simulated_outcome:
            return report

        context["simulated_outcome"] = (
            simulated_outcome
        )

        # ==========================================================
        # 17. LEARNING SYSTEM
        # ==========================================================

        learning_engine = OutcomeLearningEngine()

        learning_version = run_stage(
            "Learning Record Creation",
            learning_engine.create_learning_version,
        )

        if not learning_version:
            return report

        context["learning_version"] = (
            learning_version
        )

        # ==========================================================
        # 18. MISSION CONTROL METRICS
        # ==========================================================

        metrics = MissionControlMetrics(
            properties_analyzed=len(deal_candidates),
            markets_analyzed=len(market_summary),
            buyers_analyzed=len(buyer_events),
            deals_created=1,
            deal_rooms=1,
            opportunities_generated=len(top_matches),
            deals_closed=1,
        )

        context["mission_control_metrics"] = metrics

        report.stage_data[
            "Mission Control Metrics"
        ] = metrics

        # ==========================================================
        # FINAL WARNING
        # ==========================================================

        report.warnings.append(
            "All data is MOCK/SIMULATION and NOT LIVE DATA."
        )

        return report