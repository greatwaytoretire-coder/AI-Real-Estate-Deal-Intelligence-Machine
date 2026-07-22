# PHASE 39 — PRODUCTION READINESS

## 1. Objective

This document outlines the necessary components and strategies to prepare the AI Real Estate Deal Intelligence Machine for a production deployment. It covers database management, configuration, monitoring, and deployment procedures.

## 2. Database Migrations

The system now includes a basic schema versioning and migration capability.

- **Schema Versioning**: A `schema_version` table in the database tracks the current version.
- **Migration Execution**: The `ProductionReadinessService` contains a `run_db_migrations` method. This method should be executed as a startup task before the main application runs. It checks the current database version against the application's expected version and applies any necessary `ALTER TABLE` or other schema changes sequentially.

**Example Startup Flow:**
1.  Initialize `DatabaseClient`.
2.  Initialize `ProductionReadinessService`.
3.  Call `run_db_migrations()`.
4.  Start the main application (e.g., the `ContinuousRuntime` or API server).

## 3. Backup Strategy

- **Database**: For the SQLite database, backups can be performed by creating a file-level copy of the `.db` file. This should be done regularly (e.g., daily) using a scheduled task (like a cron job) and stored in a secure, separate location (e.g., a cloud storage bucket like AWS S3).
- **Configuration**: Environment variables and any `.env` files should be securely stored in a secret management system (e.g., AWS Secrets Manager, HashiCorp Vault).

## 4. Logging and Monitoring

- **Logging**: The existing `AuditLogger` provides a good foundation. In production, this should be configured to write to a centralized logging service (e.g., Datadog, Splunk, or an ELK stack) instead of a local file. This allows for searching, alerting, and aggregation of logs from multiple application instances.
- **Monitoring**:
  - **Health Checks**: The `ProductionReadinessService.check_health()` method provides a basic health check endpoint. This should be exposed via an API (e.g., at `/health`) and polled by a monitoring service to ensure the application and its database connection are live.
  - **Metrics**: The application should be instrumented to export key performance indicators (KPIs) to a time-series database like Prometheus. Important metrics to track include:
    - Job queue depth (`RuntimeJobQueue.pending_queue` size).
    - Number of jobs processed/failed.
    - Latency of agent execution.
    - API error rates.

## 5. Error Tracking

The application should be integrated with an error tracking service like Sentry or Bugsnag. All unhandled exceptions in the `Worker`, `AgentOrchestrator`, and any API layers should be captured and sent to this service. This provides real-time alerting, stack traces, and context for debugging production failures.

**Implementation:**
```python
# In the main application entry point
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")

# In try/except blocks for critical components
try:
    # ... run worker or agent ...
except Exception as e:
    sentry_sdk.capture_exception(e)
    # ... handle error ...
```

## 6. Configuration Management

- **Environment Variables**: The current use of environment variables via `config.py` is the correct approach.
- **Production Environment**: In production, these variables should not be set manually or stored in `.env` files on the server. They should be injected into the application's runtime environment by the deployment platform (e.g., Kubernetes Secrets, Docker Compose environment files, Heroku config vars).

## 7. Deployment

1.  **Containerization**: The application should be packaged as a Docker container. A `Dockerfile` would define the Python environment, copy the application code, and install dependencies.
2.  **Orchestration**: A container orchestration platform like Kubernetes or a PaaS like Heroku should be used to manage deployment, scaling, and environment configuration.
3.  **Deployment Process**:
    - Build the Docker image.
    - Push the image to a container registry (e.g., Docker Hub, ECR).
    - Run database migrations as a one-off task against the production database.
    - Deploy the new application version, which will pull the updated image and start the application services (e.g., the main runtime and any API servers).