# TxnVeyra

**Payment Fraud & Risk Intelligence**

TxnVeyra is a software platform foundation for payment-risk analysis, transaction assessment, relationship intelligence, and analyst investigation workflows.

## Project status

This repository contains the initial application foundation: a React frontend, a FastAPI backend, PostgreSQL persistence, dataset contract validation, and CSV ingestion.

It is not connected to UPI, NPCI, a bank, or a payment processor. It does not perform live transaction monitoring or autonomous transaction blocking. Any future demonstration stream must be explicitly identified as simulated or replayed.

## Technology stack

- React and TypeScript
- Vite
- FastAPI and Pydantic
- PostgreSQL
- SQLAlchemy and Alembic
- Pandas
- Pytest and HTTPX
- Vitest and React Testing Library
- Docker Compose

## Repository structure

```text
TxnVeyra/
├── backend/                 # API, persistence, schemas and migrations
├── frontend/                # React application
├── fraud_engine/            # Fraud rules, scoring and graph modules
├── ml/                      # Feature engineering and model workflows
├── pipelines/               # Data ingestion and validation
├── simulation/              # Reserved for controlled test-event generation
├── data/                    # Local data; not committed
├── docs/                    # Architecture and engineering decisions
├── tests/                   # Cross-module tests
├── docker-compose.yml
└── .env.example
```

## Local setup

### 1. Configure environment

Copy `.env.example` to the repository root as `.env` for Docker Compose, and copy it again to `backend/.env` for the API process. Replace every `CHANGE_ME` value with a strong local development password. Never commit either `.env` file.

### 2. Start PostgreSQL

From the repository root:

```bash
docker compose up -d db
```

### 3. Start the backend

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

### 4. Start the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite. The default is `http://localhost:5173`.

## CSV ingestion

The initial API accepts CSV files for two explicitly separated source contracts.

### `dataset_a`

Required columns:

- `txn_id`
- `timestamp`
- `fraud_flag`

### `dataset_b`

Required columns:

- `txn_id`
- `timestamp`
- `device_id`
- `is_suspicious`

Additional columns are retained in the source payload. Timestamps must be parseable and record identifiers must be present and unique within an uploaded file.

Example:

```bash
curl -X POST "http://localhost:8000/api/v1/imports/csv?source_dataset=dataset_a" \
  -F "file=@transactions.csv"
```

The importer stores source records with their dataset namespace, source record identifier, event timestamp, original row payload, and ingestion timestamp. Re-importing an existing record identifier within the same dataset does not create a duplicate.

## Development checks

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run test
npm run build
```

## Engineering principles

- Keep source datasets and their labels separate unless a verified relationship is established.
- Preserve source provenance and avoid silently changing source values.
- Do not use model outputs as ground-truth labels.
- Do not present synthetic or replayed events as live financial transactions.
- Keep secrets out of source control.
- Enforce authorization in the backend when authentication is introduced.
- Add tests with each new capability.

## Current limitations

Authentication, role-based authorization, fraud-model inference, explainability, graph analysis, case management, and production deployment are not yet implemented. The current application is a development foundation and must not be used as a production payment-control system.

## Security and data handling

- Never commit `.env` files, credentials, API keys, access tokens, certificates, or private keys.
- Use only synthetic, anonymized, or explicitly authorized data in development and demonstrations.
- Do not upload real card numbers, bank account details, UPI identifiers, customer records, or other personal financial data.
- Rotate any credential immediately if it is accidentally committed, even if the commit is later removed.
- Review `SECURITY.md` before reporting a vulnerability.
