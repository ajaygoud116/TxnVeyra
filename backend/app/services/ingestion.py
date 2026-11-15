import hashlib
import io
import json
from datetime import datetime
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ImportRun, SourceRecord
from app.services.dataset_contracts import CONTRACTS, validate_columns


class IngestionError(ValueError):
    pass


def _json_safe(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def ingest_csv(
    db: Session,
    *,
    source_dataset: str,
    filename: str,
    content: bytes,
) -> ImportRun:
    if source_dataset not in CONTRACTS:
        raise IngestionError(f"Unsupported source_dataset: {source_dataset}")
    if not content:
        raise IngestionError("Uploaded file is empty")

    digest = hashlib.sha256(content).hexdigest()
    try:
        frame = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise IngestionError(f"Unable to parse CSV: {exc}") from exc

    validate_columns(list(frame.columns), source_dataset)
    contract = CONTRACTS[source_dataset]

    if frame.empty:
        raise IngestionError("CSV contains a header but no data rows")
    if frame[contract.record_id_column].isna().any():
        raise IngestionError(f"{contract.record_id_column} contains missing values")
    if frame[contract.record_id_column].astype(str).duplicated().any():
        raise IngestionError(f"{contract.record_id_column} contains duplicate IDs")

    timestamps = pd.to_datetime(frame[contract.timestamp_column], errors="coerce", utc=True)
    if timestamps.isna().any():
        raise IngestionError(f"{contract.timestamp_column} contains invalid timestamps")

    existing_ids = set(
        db.scalars(
            select(SourceRecord.source_record_id).where(
                SourceRecord.source_dataset == source_dataset,
                SourceRecord.source_record_id.in_(frame[contract.record_id_column].astype(str).tolist()),
            )
        ).all()
    )

    records: list[SourceRecord] = []
    for index, row in frame.iterrows():
        source_id = str(row[contract.record_id_column])
        if source_id in existing_ids:
            continue
        payload = {str(k): _json_safe(v) for k, v in row.to_dict().items()}
        records.append(
            SourceRecord(
                source_dataset=source_dataset,
                source_record_id=source_id,
                event_timestamp=timestamps.iloc[index].to_pydatetime(),
                payload=payload,
            )
        )

    run = ImportRun(
        source_dataset=source_dataset,
        filename=filename[:255],
        file_sha256=digest,
        status="completed",
        rows_received=len(frame),
        rows_inserted=len(records),
        rows_skipped=len(frame) - len(records),
    )

    try:
        db.add_all(records)
        db.add(run)
        db.commit()
        db.refresh(run)
    except Exception:
        db.rollback()
        raise

    return run
