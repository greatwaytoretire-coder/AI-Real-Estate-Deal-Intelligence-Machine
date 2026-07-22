from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class MachineStatus(str, Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"


@dataclass
class OrganizationFoundation:
    organization_id: str = "demo-org"
    organization_name: str = "Demo Organization"
    environment: str = "development"


@dataclass
class AuthenticationFoundation:
    authentication_mode: str = "local-guard"
    requires_login: bool = False


@dataclass
class SystemHealth:
    database_ok: bool = True
    provider_registry_ok: bool = True
    audit_logging_ok: bool = True
    event_system_ok: bool = True

    def overall_status(self) -> str:
        checks = [
            self.database_ok,
            self.provider_registry_ok,
            self.audit_logging_ok,
            self.event_system_ok,
        ]
        if any(not check for check in checks):
            return "degraded" if all(check is not False for check in checks) else "error"
        return "healthy"


@dataclass
class EventBus:
    events: List[Dict[str, Any]] = field(default_factory=list)

    def publish(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = {"event_type": event_type, "payload": payload}
        self.events.append(event)
        return event


@dataclass
class AgentTaskQueue:
    _tasks: List[Dict[str, Any]] = field(default_factory=list)

    def enqueue(self, task_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        task = {"task_name": task_name, "payload": payload or {}}
        self._tasks.append(task)
        return task

    def size(self) -> int:
        return len(self._tasks)


@dataclass
class BackgroundJobFoundation:
    jobs: List[Dict[str, Any]] = field(default_factory=list)

    def register(self, job_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        job = {"job_name": job_name, "payload": payload or {}}
        self.jobs.append(job)
        return job


@dataclass
class ApplicationShell:
    machine_status: MachineStatus = MachineStatus.RUNNING
    navigation_sections: List[str] = field(
        default_factory=lambda: [
            "Mission Control",
            "Opportunities",
            "Markets",
            "Buyers",
            "Sellers",
            "Deals",
            "AI Agents",
            "Activity",
            "Settings",
        ]
    )

    def dashboard_sections(self) -> List[str]:
        return list(self.navigation_sections)

    def health_page(self) -> Dict[str, Any]:
        return {
            "machine_status": self.machine_status.value,
            "overall_health": SystemHealth().overall_status(),
            "sections": self.dashboard_sections(),
        }


class FoundationApp(ApplicationShell):
    """Phase 1 foundation app shell for the AI Deal Machine."""

    def __init__(self) -> None:
        super().__init__()
        self.organization = OrganizationFoundation()
        self.auth = AuthenticationFoundation()
        self.event_bus = EventBus()
        self.task_queue = AgentTaskQueue()
        self.jobs = BackgroundJobFoundation()

    def dashboard_sections(self) -> List[str]:
        return list(self.navigation_sections)

    def render_dashboard(self) -> Dict[str, Any]:
        return {
            "title": "AI Real Estate Deal Intelligence Machine",
            "machine_status": self.machine_status.value,
            "navigation": self.dashboard_sections(),
            "system_health": SystemHealth().overall_status(),
            "event_bus": len(self.event_bus.events),
            "agent_tasks": self.task_queue.size(),
        }
