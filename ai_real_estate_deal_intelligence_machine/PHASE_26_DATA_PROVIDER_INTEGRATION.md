# PHASE 26 — AUTHORIZED REAL DATA SOURCE INTEGRATION

## 1. Objective

Phase 26 establishes the architecture and methodology for integrating real-world data sources in a safe, compliant, and authorized manner. The primary goal is to create a robust framework that supports live data while strictly prohibiting unauthorized access methods like scraping or bypassing platform terms of service.

This phase ensures every data provider, whether live or mock, adheres to a consistent interface that includes configuration, error handling, source attribution, and audit logging.

## 2. Guiding Principles

All data integration must adhere to the following principles:
- **No Unauthorized Access**: The system must not bypass CAPTCHAs, login systems, rate limits, or other access controls. All platform terms of service must be respected.
- **Authorized Sources Only**: Data must come from official APIs, licensed providers, authorized feeds, legally permitted public government data, or user-provided datasets.
- **Maintain Abstraction**: The existing provider abstraction layer is extended, not replaced, ensuring that live and mock providers can be used interchangeably where appropriate.
- **Graceful Fallback**: The system must gracefully fall back to mock providers if a live provider is not configured, fails, or is disabled. This is critical for development and testing environments.
- **Clear Data Distinction**: All data must be clearly labeled with its source. Mock data must never be presented as live data.
- **Cost Control**: Providers requiring payment must be explicitly enabled by an operator and must not be activated by default.

## 3. Provider Architecture

### 3.1. `ProviderConfig`

A new `ProviderConfig` dataclass is introduced to define the metadata for any data provider. It includes:
- **`name`**: A unique identifier for the provider (e.g., `attom_api`).
- **`label`**: A human-readable name (e.g., "ATTOM Data API").
- **`source_type`**: The classification of the data source (`LIVE` or `MOCK`).
- **`api_key_env_var`**: The environment variable that holds the API key, if required.
- **`cost_per_call`**: The estimated cost for each API call, defaulting to `0.0` for free providers.

### 3.2. `DataProvider` Interface

A new abstract base class, `DataProvider`, defines the contract for all providers. It requires the implementation of:
- **`fetch()`**: The method to retrieve data.
- **`get_config()`**: A method to return its `ProviderConfig`.

This interface ensures that every provider, live or mock, exposes its configuration and capabilities in a standardized way.

### 3.3. `ProviderManager`

The `ProviderManager` is a new orchestration class responsible for initializing and managing all data providers. Its key responsibilities are:
- **Discovery and Initialization**: It discovers all available `DataProvider` subclasses.
- **Configuration Check**: For each live provider, it checks if the required API key is present in the environment.
- **Fallback Logic**: If a live provider's API key is missing, the manager automatically falls back to its corresponding mock version (e.g., `AttomApiProvider` falls back to `MockAttomProvider`). This ensures the system can always run, even without live credentials.
- **Source Attribution**: It wraps all data returned from a provider in a `PilotDataRecord`, ensuring every piece of data is stamped with its source, confidence, and freshness.

## 4. Implementation Details

### New Files

- `ai_real_estate_deal_intelligence_machine/phase26.py`: Contains the `ProviderConfig`, `DataProvider` ABC, `ProviderManager`, and the new simulated `AttomApiProvider` and its mock counterpart.
- `tests/test_phase26_data_integration.py`: A repeatable unit test that verifies the `ProviderManager`'s fallback logic and ensures data is correctly attributed.

### Example Provider: `AttomApiProvider`

To demonstrate the pattern, a new `AttomApiProvider` is implemented.
- It is configured to look for an `ATTOM_API_KEY` environment variable.
- If the key is present, it simulates making a live API call.
- If the key is absent, the `ProviderManager` ensures that the `MockAttomProvider` is used instead, and a warning is logged.
- This provider is documented with its (hypothetical) authorization requirements, cost, rate limits, and other considerations as required by this phase.

## 5. Verification and Reporting

The `test_provider_manager_fallback_and_live_mode` unit test verifies the core functionality of this phase:
1.  It runs the `ProviderManager` without setting the `ATTOM_API_KEY` and confirms that the data source is correctly identified as `MOCK`.
2.  It then simulates setting the API key and confirms that the `ProviderManager` switches to the `LIVE` provider.
3.  It verifies that all data returned is wrapped in a `PilotDataRecord` with the correct source attribution.

## 6. Cost and Compliance

### Cost Implications
- The architecture explicitly includes a `cost_per_call` field in the `ProviderConfig`. This allows the system to track and report on potential operational costs before they are incurred.
- By default, all paid providers are inactive unless an API key is provided, preventing accidental charges.

### Compliance Considerations
- The requirement for an `api_key_env_var` ensures that credentials are not hardcoded.
- The entire framework is built around using authorized APIs, aligning with legal and compliance requirements.
- The documentation template for each provider includes a section for "Legal/Compliance Considerations," ensuring these are evaluated for every new integration.

## 7. Conclusion

Phase 26 successfully creates a secure, compliant, and robust foundation for integrating real-world data providers. The `ProviderManager`'s automatic fallback logic provides essential flexibility for development and testing, while the strict configuration and data labeling requirements ensure that the system operates safely and transparently. The platform is now ready to begin integrating a curated list of authorized, live data sources.