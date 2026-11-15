# TxnVeyra Migration Plan

## Stage 1 — Repository foundation

- Establish frontend and backend project foundations.
- Configure PostgreSQL and Docker Compose.
- Add SQLAlchemy models and Alembic migrations.
- Define source dataset contracts.
- Implement validated and idempotent CSV ingestion.
- Add import-run metadata and source-record persistence.
- Add API health checks and a frontend application shell.
- Verify database migrations and end-to-end imports.

## Stage 2 — Fraud detection

- Document label generation and feature lineage.
- Define point-in-time feature contracts.
- Establish a defensible evaluation protocol.
- Implement deterministic rules, supervised classification, and anomaly detection as separate signal providers.
- Evaluate using precision-recall metrics, alert-volume constraints, and calibration.
- Persist versioned risk assessments and evidence.

## Stage 3 — Network intelligence

- Define supported entity and relationship semantics.
- Build graph analysis with provenance for every displayed edge.
- Present shared attributes as investigative leads, not proof of wrongdoing.

## Stage 4 — Investigation workflows

- Implement alerts, cases, assignments, notes, evidence snapshots, and audit history.
- Add authentication and server-side role authorization.

## Stage 5 — Frontend intelligence modules

- Implement transaction search and details.
- Implement risk views and model observability.
- Implement network exploration.
- Implement investigation workflows.
- Implement geographic and temporal analysis.
- Bind displayed metrics to API-backed data.

## Stage 6 — Production hardening

- Add continuous integration.
- Add structured logging, health checks, and operational monitoring.
- Perform security and dependency reviews.
- Document backup, restore, deployment, and incident procedures.

## Migration safeguards

- Keep source datasets separate until a verified linkage is established.
- Do not treat model outputs as ground truth.
- Do not load untrusted serialized model artifacts.
- Clearly identify simulated or replayed events.
- Use database migrations for schema changes.
- Add tests alongside each capability.
