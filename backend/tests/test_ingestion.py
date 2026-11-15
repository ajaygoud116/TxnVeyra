import pytest

from app.services.dataset_contracts import DatasetContractError
from app.services.ingestion import IngestionError, ingest_csv


def test_empty_file_is_rejected():
    with pytest.raises(IngestionError, match="empty"):
        ingest_csv(None, source_dataset="dataset_a", filename="empty.csv", content=b"")


def test_bad_csv_schema_is_rejected():
    with pytest.raises(DatasetContractError):
        ingest_csv(
            None,
            source_dataset="dataset_a",
            filename="wrong.csv",
            content=b"not_txn,not_time\n1,2024-01-01",
        )
