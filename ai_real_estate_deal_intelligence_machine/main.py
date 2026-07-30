from __future__ import annotations

from typing import Any, Dict

from .config import settings
from .audit_logger import AuditLogger
from .db_client import DatabaseClient
from .jobs.base import Job
from .phase26 import ProviderManager
from .phase29 import ScalingManager
from .phase30 import ContinuousRuntime # type: ignore
from .phase36 import AgentOrchestrator, AgentWorkflow
from .phase37 import MultiMarketOrchestrator
from .phase5 import OpportunityScoringEngine, ScoringInput
from .phase8 import DealRiskAgent, DealRiskAgentInput
from .persistent_deduplication_engine import PersistentDeduplicationEngine
from .persistent_job_queue import PersistentJobQueue
from .supervisor import SystemSupervisor


def create_production_services() -> Dict[str, Any]:
    """
    Creates and wires together all core services for the application.
    This function acts as the "composition root" for the production application.
    """
    # 1. Initialize foundational services
    db_client = DatabaseClient()
    audit_logger = AuditLogger()
    provider_manager = ProviderManager(audit_logger=audit_logger)
    scaling_manager = ScalingManager()
    orchestrator = AgentOrchestrator(audit_logger=audit_logger)


    # 2. Create production agent instances
    risk_agent = DealRiskAgent(audit_logger=audit_logger)
    scoring_agent = OpportunityScoringEngine(audit_logger=audit_logger)

    # 3. Define production input factories for the agents
    def risk_agent_factory(job: Job) -> DealRiskAgentInput:
        return DealRiskAgentInput(
            correlation_id=job.job_id,
            market_id=job.payload.get("market_id"),
            deal_id=job.payload.get("entity_id"),
        )

    def scoring_engine_factory(job: Job) -> ScoringInput:
        return ScoringInput(
            correlation_id=job.job_id,
            market_id=job.payload.get("market_id"),
            scoring_model_version=job.payload.get("scoring_model_version", "default_v1"),
        )

    # 4. Create and register the production workflow
    # This workflow defines the sequence of agents for a 'PROPERTY_DISCOVERED' event.
    production_workflow = AgentWorkflow(
        name="Standard Property Analysis",
        steps=[risk_agent, scoring_agent],
        input_factories={
            "DealRiskAgent": risk_agent_factory,
            "OpportunityScoringEngine": scoring_engine_factory,
        },
    )
    orchestrator.register_workflow("PROPERTY_DISCOVERED", production_workflow)

    # 5. Create persistent components for the production runtime
    persistent_job_queue = PersistentJobQueue(db_client=db_client)
    persistent_deduplication_engine = PersistentDeduplicationEngine(db_client=db_client)

    # Recover any jobs that were stuck in a RUNNING state from a previous crash
    recovered_count = persistent_job_queue.recover_stale_jobs(settings.STALE_JOB_TIMEOUT_SECONDS)
    if recovered_count > 0:
        audit_logger.log("RECOVERY", f"Recovered {recovered_count} stale jobs from previous run.")

    # 6. Create the main ContinuousRuntime with persistent components injected
    runtime = ContinuousRuntime(
        audit_logger=audit_logger,
        provider_manager=provider_manager,
        orchestrator=orchestrator,
        scaling_manager=scaling_manager,
        job_queue=persistent_job_queue,
        deduplication_engine=persistent_deduplication_engine,
    )

    # 7. Create high-level orchestrators
    multi_market_orchestrator = MultiMarketOrchestrator(scaling_manager=scaling_manager, runtime=runtime)

    # Return all components for the main function or tests to use
    # Note: db_client is not returned as it's encapsulated by the persistent components.
    return {
    "runtime": runtime,
    "orchestrator": orchestrator,
    "provider_manager": provider_manager,
    "scaling_manager": scaling_manager,
    "multi_market_orchestrator": multi_market_orchestrator,
    "audit_logger": audit_logger,
    "db_client": db_client,
}


def main():
    """The main entry point for the application."""
    print("Initializing AI Real Estate Deal Intelligence Machine...")
    services = create_production_services()
    print("Bootstrap complete. Starting System Supervisor...")
    supervisor = SystemSupervisor(**services)
    supervisor.run_continuously()


if __name__ == "__main__":
    main()