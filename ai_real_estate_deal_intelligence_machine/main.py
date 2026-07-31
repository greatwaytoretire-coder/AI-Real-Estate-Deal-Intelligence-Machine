from __future__ import annotations

from typing import Any, Dict

from .config import settings
from .audit_logger import AuditLogger
from .db_client import DatabaseClient
from .jobs.base import Job

from .phase26 import ProviderManager

from .phase29 import (
    ScalingManager,
    MarketConfig,
    MarketStatus,
)

from .phase30 import ContinuousRuntime

from .phase36 import (
    AgentOrchestrator,
    AgentWorkflow,
)

from .phase37 import MultiMarketOrchestrator

from .phase5 import (
    OpportunityScoringEngine,
    ScoringInput,
)

from .phase8 import (
    DealRiskAgent,
    DealRiskAgentInput,
)

from .persistent_deduplication_engine import (
    PersistentDeduplicationEngine,
)

from .persistent_job_queue import (
    PersistentJobQueue,
)

from .supervisor import SystemSupervisor


def create_production_services() -> Dict[str, Any]:
    """
    Production dependency composition root.
    Creates and wires all application services.
    """

    # --------------------------------------------------
    # Core infrastructure
    # --------------------------------------------------

    db_client = DatabaseClient()

    audit_logger = AuditLogger()

    provider_manager = ProviderManager(
        audit_logger=audit_logger
    )

    scaling_manager = ScalingManager()


    # --------------------------------------------------
    # Register active markets
    # --------------------------------------------------

    scaling_manager.load_market_config(
        MarketConfig(
            market_id="test_market",
            market_name="Test Market",
            status=MarketStatus.ACTIVE,
            data_providers=[
                "attom"
            ],
        )
    )


    # --------------------------------------------------
    # AI Agent Orchestration
    # --------------------------------------------------

    orchestrator = AgentOrchestrator(
        audit_logger=audit_logger
    )


    risk_agent = DealRiskAgent(
        audit_logger=audit_logger
    )

    scoring_agent = OpportunityScoringEngine(
        audit_logger=audit_logger
    )


    # --------------------------------------------------
    # Agent Input Factories
    # --------------------------------------------------

    def risk_agent_factory(
        job: Job
    ) -> DealRiskAgentInput:

        return DealRiskAgentInput(
            correlation_id=job.job_id,
            market_id=job.payload.get(
                "market_id"
            ),
            deal_id=job.payload.get(
                "entity_id"
            ),
        )


    def scoring_engine_factory(
        job: Job
    ) -> ScoringInput:

        return ScoringInput(
            correlation_id=job.job_id,
            market_id=job.payload.get(
                "market_id"
            ),
            scoring_model_version=job.payload.get(
                "scoring_model_version",
                "default_v1",
            ),
        )


    production_workflow = AgentWorkflow(
        name="Standard Property Analysis",
        steps=[
            risk_agent,
            scoring_agent,
        ],
        input_factories={
            "DealRiskAgent": risk_agent_factory,
            "OpportunityScoringEngine": scoring_engine_factory,
        },
    )


    orchestrator.register_workflow(
        "PROPERTY_DISCOVERED",
        production_workflow,
    )


    # --------------------------------------------------
    # Persistent Runtime Components
    # --------------------------------------------------

    persistent_job_queue = PersistentJobQueue(
        db_client=db_client
    )


    persistent_deduplication_engine = (
        PersistentDeduplicationEngine(
            db_client=db_client
        )
    )


    recovered_count = (
        persistent_job_queue.recover_stale_jobs(
            settings.STALE_JOB_TIMEOUT_SECONDS
        )
    )


    if recovered_count:

        audit_logger.log(
            "RECOVERY",
            (
                f"Recovered "
                f"{recovered_count} stale jobs."
            ),
        )


    # --------------------------------------------------
    # Continuous Runtime
    # --------------------------------------------------

    runtime = ContinuousRuntime(
        audit_logger=audit_logger,
        provider_manager=provider_manager,
        orchestrator=orchestrator,
        scaling_manager=scaling_manager,
        job_queue=persistent_job_queue,
        deduplication_engine=
            persistent_deduplication_engine,
    )


    # --------------------------------------------------
    # Multi Market Supervisor Layer
    # --------------------------------------------------

    multi_market_orchestrator = (
        MultiMarketOrchestrator(
            scaling_manager=scaling_manager,
            runtime=runtime,
        )
    )


    return {

        "runtime": runtime,

        "orchestrator": orchestrator,

        "provider_manager": provider_manager,

        "scaling_manager": scaling_manager,

        "multi_market_orchestrator":
            multi_market_orchestrator,

        "audit_logger": audit_logger,

        "db_client": db_client,
    }



def main():

    print(
        "Initializing AI Real Estate Deal Intelligence Machine..."
    )


    services = create_production_services()


    print(
        "Bootstrap complete. Starting System Supervisor..."
    )


    supervisor = SystemSupervisor(

        multi_market_orchestrator=
            services[
                "multi_market_orchestrator"
            ],

        runtime=
            services[
                "runtime"
            ],

        audit_logger=
            services[
                "audit_logger"
            ],
    )


    supervisor.run_continuously()



if __name__ == "__main__":

    main()