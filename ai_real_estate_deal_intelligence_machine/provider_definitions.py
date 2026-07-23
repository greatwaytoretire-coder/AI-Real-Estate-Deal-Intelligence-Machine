from __future__ import annotations

from .phase31 import AttomDataDownloader
from .providers.mock_providers import MockAttomProvider

PROVIDER_DEFINITIONS = {
    "attom": {
        "live": AttomDataDownloader,
        "mock": MockAttomProvider,
        "api_key_env_var": "ATTOM_API_KEY",
    }
}
