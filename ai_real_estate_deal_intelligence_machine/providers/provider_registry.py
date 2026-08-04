from __future__ import annotations

from typing import Dict, List

from .base import DataProvider
from .provider_types import ProviderStatus


class ProviderRegistry:
    """
    Central registry for all intelligence data providers.

    Handles provider registration, discovery,
    and retrieval for the AI Deal Intelligence Machine.
    """

    def __init__(self):
        self._providers: Dict[str, DataProvider] = {}
        self._statuses: Dict[str, ProviderStatus] = {}

    def register_provider(
        self,
        provider: DataProvider,
        status: ProviderStatus = ProviderStatus.ACTIVE,
    ) -> None:
        """
        Register a provider with the system.
        """

        config = provider.get_config()

        self._providers[config.name] = provider
        self._statuses[config.name] = status

    def get_provider(
        self,
        provider_name: str,
    ) -> DataProvider:
        """
        Retrieve a provider by name.
        """

        if provider_name not in self._providers:
            raise KeyError(
                f"Provider '{provider_name}' is not registered."
            )

        return self._providers[provider_name]

    def list_providers(self) -> List[str]:
        """
        Return all registered provider names.
        """

        return list(self._providers.keys())

    def get_status(
        self,
        provider_name: str,
    ) -> ProviderStatus:
        """
        Return provider status.
        """

        if provider_name not in self._statuses:
            raise KeyError(
                f"Provider '{provider_name}' is not registered."
            )

        return self._statuses[provider_name]

    def remove_provider(
        self,
        provider_name: str,
    ) -> None:
        """
        Remove provider from registry.
        """

        self._providers.pop(provider_name, None)
        self._statuses.pop(provider_name, None)

    def clear(self) -> None:
        """
        Clear all providers.
        """

        self._providers.clear()
        self._statuses.clear()