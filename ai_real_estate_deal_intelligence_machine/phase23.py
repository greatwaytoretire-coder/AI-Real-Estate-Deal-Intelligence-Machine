from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .phase3 import MarketIntelligenceAgent, MarketScore
from .phase4 import PropertyDiscoveryAgent, PropertyProfile
from .phase5 import DealScorecard, OpportunityScoringEngine
from .phase6 import ARVAnalysisAgent, ComparableSalesAgent, RepairEstimationAgent
from .phase7 import DealUnderwritingAgent, UnderwritingResult
from .phase8 import DealRiskAgent, RiskAssessment
from .phase9 import BuyerIntelligenceEngine, BuyerProfile
from .phase10 import BuyerMatchingEngine, BuyerRankedMatch
from .phase11 import SellerAcquisitionAgent, SellerOpportunity
from .phase13 import DealRoomAgent, DealRoomMetrics
from .phase14 import DealLifecycleWorkflow
from .phase15 import LearningVersion, OutcomeLearningEngine
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
        """Executes the full simulation and returns a report."""
        report = EndToEndSimulationReport()
        context: Dict[str, Any] = {}

        # Helper to run and report on each stage
        def run_stage(stage_name: str, func, *args, **kwargs):
            try:
                result = func(*args, **kwargs)
                report.stages_completed.append(stage_name)
                report.stage_data[stage_name] = result
                return result
            except Exception as e:
                error_message = f"Stage '{stage_name}' failed: {e}"
                report.stages_failed[stage_name] = error_message
                report.errors.append(error_message)
                return None

        # 1. Market Intelligence
        market_agent = MarketIntelligenceAgent()
        market_summary = run_stage("Market Intelligence", market_agent.run_mock_analysis)
        if not market_summary:
            return report
        context["market_summary"] = market_summary
        context["market_score"] = market_summary.market_score

        # 2. Property Discovery
        property_agent = PropertyDiscoveryAgent()
        property_profile = run_stage("Property Discovery", property_agent.discover_mock_property)
        if not property_profile:
            return report
        context["property_profile"] = property_profile

        # 3. Seller Motivation Signals
        seller_agent = SellerAcquisitionAgent()
        seller_opportunity = run_stage("Seller Motivation", seller_agent.run_mock_qualification)
        if not seller_opportunity:
            return report
        context["seller_opportunity"] = seller_opportunity

        # 4. Comparable Sales
        comps_agent = ComparableSalesAgent()
        comp_set = run_stage("Comparable Sales", comps_agent.get_mock_comps, property_profile)
        if not comp_set:
            return report
        context["comp_set"] = comp_set

        # 5. Underwriting (ARV, Repair, Costs)
        arv_agent = ARVAnalysisAgent()
        arv_estimate = run_stage("ARV Calculation", arv_agent.estimate_arv, comp_set)
        if not arv_estimate:
            return report
        context["arv_estimate"] = arv_estimate

        repair_agent = RepairEstimationAgent()
        repair_estimate = run_stage("Repair Estimation", repair_agent.estimate_repairs, property_profile)
        if not repair_estimate:
            return report
        context["repair_estimate"] = repair_estimate

        underwriting_agent = DealUnderwritingAgent()
        underwriting_result = run_stage(
            "Underwriting",
            underwriting_agent.run_mock_underwriting,
            arv_estimate,
            repair_estimate,
        )
        if not underwriting_result:
            return report
        context["underwriting_result"] = underwriting_result

        # 6. Deal & Risk Scoring
        scoring_engine = OpportunityScoringEngine()
        deal_scorecard = run_stage(
            "Deal Scoring",
            scoring_engine.score_opportunity,
            property_profile,
            market_summary,
            underwriting_result,
        )
        if not deal_scorecard:
            return report
        context["deal_scorecard"] = deal_scorecard
        report.final_deal_score = deal_scorecard.deal_potential_score

        risk_agent = DealRiskAgent()
        risk_assessment = run_stage("Risk Scoring", risk_agent.assess_mock_risk, property_profile)
        if not risk_assessment:
            return report
        context["risk_assessment"] = risk_assessment
        report.final_risk_score = risk_assessment.risk_score

        # 7. Buyer Discovery & Analysis
        buyer_engine = BuyerIntelligenceEngine()
        buyer_profiles = run_stage("Buyer Discovery", buyer_engine.discover_mock_buyers)
        if not buyer_profiles:
            return report
        context["buyer_profiles"] = buyer_profiles

        # 8. Buyer Matching
        buyer_matching_engine = BuyerMatchingEngine()
        buyer_matches = run_stage(
            "Buyer Matching",
            buyer_matching_engine.find_matches,
            deal_scorecard,
            buyer_profiles,
        )
        if not buyer_matches:
            return report
        context["buyer_matches"] = buyer_matches
        if buyer_matches:
            report.final_buyer_match_score = buyer_matches[0].match_score

        # 9. Deal Packaging
        deal_room_agent = DealRoomAgent()
        deal_room_metrics = run_stage(
            "Deal Packaging",
            deal_room_agent.create_mock_deal_room,
            property_profile,
            underwriting_result,
            risk_assessment,
        )
        if not deal_room_metrics:
            return report
        context["deal_room_metrics"] = deal_room_metrics
        report.final_deal_package = {
            "deal_room_id": deal_room_metrics.deal_room_id,
            "status": "Investor-Ready Package (SIMULATION)",
            "property_address": property_profile.address,
            "arv": underwriting_result.arv,
            "estimated_profit": underwriting_result.estimated_profit,
            "risk_score": risk_assessment.risk_score,
        }

        # 10. Workflow Preparation
        lifecycle_workflow = run_stage("Workflow Preparation", DealLifecycleWorkflow)
        if not lifecycle_workflow:
            return report
        context["lifecycle_workflow"] = lifecycle_workflow

        # 11. Simulated Outcome Recording
        # In a real system, this would come from an external event. Here, we simulate it.
        simulated_outcome = run_stage(
            "Outcome Recording",
            lambda: {
                "outcome": "CLOSED_DEAL",
                "final_price": 400000,
                "notes": "Simulated successful closing.",
            },
        )
        if not simulated_outcome:
            return report
        context["simulated_outcome"] = simulated_outcome

        # 12. Learning Record Creation
        learning_engine = OutcomeLearningEngine()
        learning_version = run_stage(
            "Learning Record Creation",
            learning_engine.process_outcome,
            deal_scorecard,
            simulated_outcome,
        )
        if not learning_version:
            return report
        context["learning_version"] = learning_version

        report.warnings.append("All data is MOCK/SIMULATION and NOT LIVE DATA.")

        return report