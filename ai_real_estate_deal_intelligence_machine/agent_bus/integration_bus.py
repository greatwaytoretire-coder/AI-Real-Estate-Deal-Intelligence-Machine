from typing import Dict, Callable

from .agent_bus_models import (
    AgentRequest,
    AgentResponse,
)


class AgentIntegrationBus:

    def __init__(self):
        self.agents: Dict[str, Callable] = {}

    def register_agent(
        self,
        name: str,
        handler: Callable,
    ):
        self.agents[name] = handler

    def execute(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        if request.agent_name not in self.agents:
            return AgentResponse(
                agent_name=request.agent_name,
                success=False,
                result=None,
                message="Agent not registered.",
            )

        result = self.agents[
            request.agent_name
        ](
            request.payload
        )

        return AgentResponse(
            agent_name=request.agent_name,
            success=True,
            result=result,
            message="Agent execution completed.",
        )