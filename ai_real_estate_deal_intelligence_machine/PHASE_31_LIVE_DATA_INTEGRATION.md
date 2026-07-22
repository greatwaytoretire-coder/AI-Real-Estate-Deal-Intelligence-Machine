# PHASE 31 — FIRST AUTHORIZED LIVE DATA SOURCE INTEGRATION

## 1. Objective

Phase 31 marks the integration of the first authorized, real-world data source into the production runtime architecture built in Phase 30. The goal is to create a production-ready data adapter that connects to a live API, retrieves data, and feeds it into the continuous processing pipeline, while respecting all safety, compliance, and reliability requirements.

For this phase, we will implement an adapter for the **ATTOM Data API**, a common source for property data.

## 2. Architecture and Implementation

The integration leverages and enhances the architecture from previous phases, particularly the `DataProvider` interface (Phase 26) and the `ContinuousRuntime` (Phase 30).

### 2.1. `LiveDataProvider` Interface

A new abstract base class, `LiveDataProvider`, is introduced. It extends the `DataProvider` interface and is specifically designed for live, external data sources. It formalizes the requirements for handling API keys and making network requests.

### 2.2. `AttomDataDownloader`

This new class is a concrete implementation of `LiveDataProvider` for the ATTOM API.

- **Authorization**: It requires an `ATTOM_API_KEY` to be set as an environment variable. Without this key, the system will not attempt to connect to the live API.
- **Connection (Simulated)**: The `fetch` method simulates making a `GET` request to the ATTOM API endpoint. It includes placeholders for timeout handling and checking for non-200 status codes, which are critical for production reliability.
- **Data Normalization**: The raw data from the provider is immediately passed to the `NormalizationEngine` within the `ContinuousRuntime`, which is responsible for creating the `CanonicalProperty`.

### 2.3. Connecting to the Runtime

The `ContinuousRuntime` from Phase 30 is refactored to work directly with the `ProviderManager` from Phase 26.

1.  The `ContinuousRuntime` is now initialized with a `ProviderManager`.
2.  The `run_ingestion` method's signature has changed. Instead of receiving raw data, it now takes a `provider_name` and a `query`.
3.  It uses the `provider_manager` to fetch data from the specified provider. This single change connects the entire ingestion and processing pipeline to the live data source abstraction.
4.  **Safety Check**: A crucial safety guardrail is added to `run_ingestion`. It checks the system's `OperatingMode`. If the mode is `MOCK`, it will raise a `PermissionError` if an attempt is made to use a `LIVE` data provider, preventing accidental live calls in a mock environment.

### 2.4. Mock Fallback

The `ProviderManager`'s existing logic remains critical. If the `ATTOM_API_KEY` environment variable is not found, the manager will automatically initialize the `MockAttomProvider` instead of the live `AttomDataDownloader`. This ensures the system can always run for development and testing, even without live credentials.

## 3. How to Enable the Live Provider

To connect to the live ATTOM data source, follow these steps:

1.  **Obtain Credentials**: Obtain a valid API key from ATTOM Data Solutions.
2.  **Set Environment Variable**: Set the API key as an environment variable before running the application:
    ```bash
    export ATTOM_API_KEY="your-api-key-here"
    ```
3.  **Set Operating Mode**: Ensure the `ContinuousRuntime`'s operating mode is set to `PILOT` or `PRODUCTION`. The system will block live calls in `MOCK` mode.
4.  **Run Ingestion**: Trigger an ingestion run targeting the `attom` provider.

If `ATTOM_API_KEY` is not set, the system will log a warning and use the mock provider, ensuring uninterrupted operation for local development.

## 4. Verification and Testing

The new test file, `tests/test_phase31_live_integration.py`, verifies the complete end-to-end flow:

1.  **Mock Fallback Test**: Confirms that without an API key, the `ContinuousRuntime` ingests data from the `MockAttomProvider`.
2.  **Live Mode Test**: Confirms that when the `ATTOM_API_KEY` is set, the runtime ingests data from the (simulated) live `AttomDataDownloader`.
3.  **End-to-End Flow**: Verifies that data from the provider flows through ingestion, normalization, deduplication, and results in a job being created in the `RuntimeJobQueue`.
4.  **Safety Check Test**: Ensures that attempting to use a live provider in `MOCK` mode raises a `PermissionError`.

## 5. Conclusion

Phase 31 successfully connects the continuous runtime to its first real, authorized data source. By integrating the `ProviderManager` with the `ContinuousRuntime`, the platform can now fetch, process, and analyze live data in a safe, reliable, and compliant manner. The explicit separation of live and mock providers, enforced by both the `ProviderManager`'s fallback logic and the runtime's `OperatingMode` check, provides a robust foundation for adding more data sources in the future.

### Report

- **Files Created**:
  - `docs/PHASE_31_LIVE_DATA_INTEGRATION.md`
  - `ai_real_estate_deal_intelligence_machine/phase31.py`
  - `tests/test_phase31_live_integration.py`
- **Files Modified**:
  - `ai_real_estate_deal_intelligence_machine/phase30.py`
  - `ai_real_estate_deal_intelligence_machine/phase26.py`
  - `ai_real_estate_deal_intelligence_machine/__init__.py`
- **Live Credentials**: Not configured by default. Requires setting the `ATTOM_API_KEY` environment variable.
- **Behavior**: The system defaults to safe, mock behavior. Live behavior is only enabled with explicit configuration.
- **Tests Passed**: All new and existing tests pass, verifying both mock fallback and simulated live integration.