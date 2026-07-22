# PHASE 32 — ONE-MARKET LIVE PILOT

## 1. Objective

Phase 32 transitions the AI Real Estate Deal Intelligence Machine from architectural development to a controlled, live pilot in a single, well-defined geographic market. The goal is to run the continuous ingestion and analysis pipeline against real data, applying strict filtering criteria to focus only on relevant opportunities and generating a detailed report of the findings.

This phase operates under the existing human-in-the-loop safety controls. No automated outreach to sellers or buyers will occur.

## 2. Key Capabilities

### 2.1. Detailed Market Configuration

A new `LivePilotConfig` object provides granular control over the pilot's scope. This configuration allows an operator to define not just the market, but the specific investment strategy within it.

The configuration includes:
- **Geographic Filters**: Market name, state, county, and a specific list of target ZIP codes.
- **Property Criteria**: Property types, price range, square footage, and minimum bedrooms.
- **Deal Criteria**: Minimum estimated profit and minimum deal score for an opportunity to be considered.
- **Investment Strategy**: A label for the type of investment being targeted (e.g., "Fix and Flip").

### 2.2. One-Market Pilot Workflow

A new `LivePilotRunner` orchestrates the end-to-end workflow for the configured market. It ensures that only data matching the `LivePilotConfig` is processed.

The workflow is as follows:

1.  **Data Ingestion**: The `ContinuousRuntime` fetches data from the authorized live source (e.g., ATTOM API).
2.  **One-Market Filtering**: The `LivePilotRunner` immediately filters the ingested `CanonicalProperty` records against the geographic and property criteria in the `LivePilotConfig`.
3.  **AI Pipeline Execution**: For each filtered property, a job is created and processed by a `Worker`, which runs the full AI analysis pipeline (underwriting, scoring, etc.).
4.  **Ranking**: All successfully analyzed opportunities are collected and ranked.
5.  **Reporting**: A comprehensive `PilotReport` is generated, summarizing the results of the run.

### 2.3. Market Ranking and Heat Maps

A new `MarketRankingEngine` analyzes the opportunities processed during the pilot to generate heat-map-ready data. It aggregates metrics by ZIP code to identify which sub-areas within the market have the highest concentration of opportunities, providing valuable insights for focusing future efforts.

### 2.4. Pilot Dashboard Report

The `PilotReport` dataclass provides a structured summary of the pilot run, including:
- Total opportunities processed and rejected.
- A list of the top-ranked opportunities that met all criteria.
- For each top opportunity: deal score, confidence, data source, and warnings.
- A market heat map ranking ZIP codes by opportunity volume.
- A summary of limitations, such as missing data or provider failures.

## 3. Implementation Details

### New Files

- `docs/PHASE_32_ONE_MARKET_LIVE_PILOT.md`: This documentation file.
- `ai_real_estate_deal_intelligence_machine/phase32.py`: Contains the `LivePilotConfig`, `MarketRankingEngine`, `PilotReport`, and the `LivePilotRunner`.
- `tests/test_phase32_live_pilot.py`: A repeatable unit test that defines a pilot configuration, runs the pilot with mock data, and verifies the filtering, ranking, and reporting logic.

### Key Logic

- **`LivePilotRunner`**: This is the main entry point for the phase. It takes a `LivePilotConfig` and a `ContinuousRuntime` and orchestrates the entire process.
- **Filtering Logic**: The `_filter_opportunities` method within the `LivePilotRunner` is responsible for applying the strict criteria from the configuration. This ensures that the AI pipeline only spends resources on relevant properties.
- **Separation of Concerns**: The `LivePilotRunner` orchestrates the pilot, while the `ContinuousRuntime` remains responsible for the generic mechanics of ingestion and job processing. This keeps the architecture clean and modular.

## 4. Verification and Reporting

The `test_one_market_live_pilot_workflow` unit test verifies the complete process:

1.  A `LivePilotConfig` is created for a specific market (Austin, TX) with detailed criteria.
2.  The `LivePilotRunner` is executed with a set of mock `CanonicalProperty` records.
3.  The test asserts that properties not matching the ZIP code or property criteria are correctly filtered out and rejected.
4.  It confirms that the remaining opportunities are processed and ranked.
5.  It verifies that the final `PilotReport` contains the correct counts for processed/rejected opportunities and that the top-ranked deal matches expectations.
6.  It checks that the market ranking engine correctly aggregates opportunity counts by ZIP code.

## 5. Conclusion

Phase 32 successfully implements the machinery for a controlled, single-market live pilot. The combination of a detailed configuration (`LivePilotConfig`) and an orchestration engine (`LivePilotRunner`) allows the platform to focus its powerful analytical capabilities on a specific investment strategy. The structured `PilotReport` provides the necessary visibility to monitor performance, validate AI-driven insights, and make informed decisions about future expansion. The system is now ready to run its first live, human-supervised pilot in a production environment.