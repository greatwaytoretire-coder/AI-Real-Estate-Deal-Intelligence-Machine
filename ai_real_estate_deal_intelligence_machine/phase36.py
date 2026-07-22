from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from typing import List
from .audit_logger import AuditLogger
from .phase30 import Job


@dataclass
class AgentContract:
    """A standardized contract defining an AI agent's purpose and capabilities."""

    agent_name: str
    purpose: str
    version: str = "1.0.0"
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    audit_requirements: str = "All inputs, outputs, and errors must be logged."


@dataclass
class AgentInput:
    """Base class for agent inputs, providing a correlation ID for tracking."""

    correlation_id: str
    market_id: Optional[str] = None


@dataclass
class AgentOutput:
    """Base class for agent outputs, including confidence and error handling."""

    confidence: float = 0.0
    error: Optional[str] = None


class AIAgent(ABC):
    """An abstract base class for all AI agents, enforcing a standard contract."""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger

    @abstractmethod
    def get_contract(self) -> AgentContract:
        """Returns the agent's standardized contract."""
        pass

    @abstractmethod
    def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Executes the agent's mission."""
        pass


@dataclass
class AgentWorkflow:
    """Defines a sequence of agents to execute for a given workflow."""
    name: str
    steps: List[AIAgent]


class AgentOrchestrator:
    """
    Phase 36: The central orchestrator that coordinates AI agents based on events and jobs.
    """

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.workflow_registry: Dict[str, AgentWorkflow] = {}

    def register_workflow(self, event_type: str, workflow: AgentWorkflow):
        """Registers a workflow to handle a specific event type."""
        self.audit_logger.log("ORCHESTRATOR_SETUP", f"Registering workflow '{workflow.name}' for event type {event_type}")
        self.workflow_registry[event_type] = workflow

    def handle_job(self, job: Job) -> AgentOutput:
        """Handles a job by executing the appropriate registered workflow."""
        event_type = job.payload.get("event_type")
        if not event_type:
            return AgentOutput(error=f"Job {job.job_id} has no event_type in payload.")

        workflow = self.workflow_registry.get(event_type)
        if not workflow:
            return AgentOutput(error=f"No workflow registered for event_type {event_type} in job {job.job_id}.")

        self.audit_logger.log("ORCHESTRATOR_WORKFLOW_START", f"Starting workflow '{workflow.name}' for job {job.job_id}.")

        market_id = job.payload.get("market_id")
        last_output: AgentOutput = AgentOutput()
        for agent in workflow.steps:
            # In a real system, the output of one agent would be mapped to the input of the next.
            # For this simulation, we just execute them in sequence.
            agent_input = AgentInput(correlation_id=job.job_id, market_id=market_id)
            last_output = agent.execute(agent_input)
            if last_output.error:
                self.audit_logger.log("ORCHESTRATOR_WORKFLOW_FAIL", f"Workflow '{workflow.name}' failed at step '{agent.get_contract().agent_name}'.")
                return last_output

        self.audit_logger.log("ORCHESTRATOR_WORKFLOW_SUCCESS", f"Workflow '{workflow.name}' completed for job {job.job_id}.")
        return last_output