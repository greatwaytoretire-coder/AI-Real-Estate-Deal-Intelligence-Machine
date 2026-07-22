from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RuleCondition:
    field: str
    operator: str
    value: float


@dataclass
class RuleAction:
    name: str
    sequence: int


@dataclass
class WorkflowRule:
    trigger: str
    conditions: List[RuleCondition]
    actions: List[RuleAction]
    daily_limits: Dict[str, int]
    geographic_restrictions: List[str]
    market_restrictions: List[str]
    property_restrictions: List[str]
    communication_limits: Dict[str, int]
    follow_up_rules: List[str]
    traceability: Dict[str, str]


class WorkflowConfigurationEngine:
    """Phase 17 workflow configuration foundation."""

    def create_rule(self) -> WorkflowRule:
        return WorkflowRule(
            trigger="Opportunity Score >= 85",
            conditions=[
                RuleCondition(field="Opportunity Score", operator=">=", value=85),
                RuleCondition(field="Risk Score", operator="<=", value=30),
                RuleCondition(field="Buyer Demand", operator=">=", value=75),
            ],
            actions=[
                RuleAction(name="Create underwriting", sequence=1),
                RuleAction(name="Generate seller qualification workflow", sequence=2),
                RuleAction(name="Identify top 20 buyers", sequence=3),
                RuleAction(name="Create deal room", sequence=4),
                RuleAction(name="Begin configured outreach sequence", sequence=5),
            ],
            daily_limits={"outreach": 25, "follow_up": 10},
            geographic_restrictions=["Austin, TX"],
            market_restrictions=["single-family"],
            property_restrictions=["fix-and-flip"],
            communication_limits={"messages_per_day": 3},
            follow_up_rules=["follow up after 24 hours if no response"],
            traceability={
                "rule": "workflow-rule-001",
                "agent": "BuyerDispositionAgent",
                "trigger": "Opportunity Score >= 85",
                "decision": "Create underwriting and outreach sequence",
            },
        )

    def create_actions(self, rule: WorkflowRule) -> List[Dict[str, Any]]:
        return [
            {
                "name": action.name,
                "sequence": action.sequence,
                "traceability": rule.traceability,
            }
            for action in rule.actions
        ]
