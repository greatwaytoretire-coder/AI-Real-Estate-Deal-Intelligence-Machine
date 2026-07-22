from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .phase26 import DataProvider, ProviderConfig
from .phase24 import DataSourceType


class LiveDataProvider(DataProvider, ABC):
    """Abstract base class for providers connecting to live, external data sources."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(f"API key is required for {self.__class__.__name__}.")
        self.api_key = api_key


class AttomDataDownloader(LiveDataProvider):
    """
    Phase 31: The first production-ready data adapter for a live, authorized source.
    This class connects to the ATTOM Data API to download property data.
    """

    def get_config(self) -> ProviderConfig:
        return ProviderConfig(
            name="attom_api",
            label="ATTOM API",
            source_type=DataSourceType.LIVE,
            api_key_env_var="ATTOM_API_KEY",
            cost_per_call=0.05,
        )

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Simulates fetching data from the live ATTOM API.
        In a real implementation, this would use a library like `requests`
        to make a GET request to the ATTOM API endpoint with self.api_key.
        It would include timeout handling and check for non-200 status codes.
        """
        print(f"SIMULATING LIVE API CALL to ATTOM with query: {query}")
        # This mock response includes the fields needed for normalization.
        return [
            {"id": "attom-live-record-001", "provider": "attom_api", "address": "789 Live Way", "zip": "54321"}
        ]