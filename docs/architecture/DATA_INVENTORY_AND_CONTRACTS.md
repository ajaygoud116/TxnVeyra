# TxnVeyra Data Contracts

## Source contract: dataset_a

Required columns:

- `txn_id`
- `timestamp`
- `fraud_flag`

## Source contract: dataset_b

Required columns:

- `txn_id`
- `timestamp`
- `device_id`
- `is_suspicious`

The two contracts represent separate source namespaces. Their identifiers and labels must not be treated as interchangeable.

## Validation rules

- The uploaded file must be a valid CSV.
- Required columns must be present.
- The record identifier must not be null.
- Record identifiers must be unique within one uploaded file.
- Event timestamps must parse successfully.
- The configured upload-size limit must be respected.

Additional source columns are retained in the original row payload.

## Persistence contract

Each imported source record stores:

- Source dataset namespace
- Source record identifier
- Event timestamp
- Original row payload
- Ingestion timestamp

The unique key `(source_dataset, source_record_id)` prevents duplicate persistence across repeated imports.

Import-run metadata stores the filename, SHA-256 file checksum, row counts, status, and creation timestamp.

## Provenance requirements

Before using a dataset for public claims or model evaluation, document its origin, licensing, generation method, label semantics, and known limitations. Preserve source values and record validation outcomes.
