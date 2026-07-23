from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# This import is adjusted to be relative to the new location
from ..audit_logger import AuditLogger


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
    def get_contract(self) -> "AgentContract":
        """Returns the agent's standardized contract."""
        pass

    @abstractmethod
    def execute(self, agent_input: "AgentInput") -> "AgentOutput":
        """Executes the agent's mission."""
        pass
