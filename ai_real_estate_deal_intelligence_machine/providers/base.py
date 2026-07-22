from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ProviderRecord:
    name: str
    label: str
    source_type: str = "mock"
    enabled: bool = True


class BaseProvider(ABC):
    """Abstract provider interface for Phase 0."""

    @property
    @abstractmethod
    def record(self) -> ProviderRecord:
        raise NotImplementedError

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
