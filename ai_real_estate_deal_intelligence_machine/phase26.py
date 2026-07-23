from __future__ import annotations

import os
from typing import Any, Dict, List

from .audit_logger import AuditLogger
from .provider_definitions import PROVIDER_DEFINITIONS
from .providers.base import DataProvider


class ProviderManager:
    """Manages data providers, including fallback from live to mock."""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.providers: Dict[str, DataProvider] = self._initialize_providers(
            PROVIDER_DEFINITIONS
        )

    def _initialize_providers(self, registry: Dict) -> Dict[str, DataProvider]:
        """
        Initializes providers from a registry, respecting API key availability.
        Falls back to mocks if keys are not found.
        """
        initialized_providers: Dict[str, DataProvider] = {}

        for provider_name, definition in registry.items():
            live_class = definition["live"]
            mock_class = definition["mock"]
            api_key_env_var = definition.get("api_key_env_var")
            api_key = os.getenv(api_key_env_var) if api_key_env_var else None

            if api_key:
                # Assumes live provider takes api_key if it's required
                try:
                    provider = live_class(api_key=api_key)
                except TypeError:
                    provider = live_class()
                self.audit_logger.log(
                    "PROVIDER_INIT",
                    f"Initialized LIVE provider: {provider.get_config().label}",
                )
            else:
                provider = mock_class()
                self.audit_logger.log(
                    "PROVIDER_INIT",
                    f"API key for {provider_name} not found. Falling back to MOCK provider: {provider.get_config().label}",
                )

            initialized_providers[provider_name] = provider

        return initialized_providers