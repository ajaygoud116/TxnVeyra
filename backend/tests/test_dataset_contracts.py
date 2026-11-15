import pytest

from app.services.dataset_contracts import DatasetContractError, validate_columns


def test_dataset_a_contract_accepts_required_columns():
    validate_columns(["txn_id", "timestamp", "fraud_flag", "amount"], "dataset_a")


def test_dataset_b_contract_accepts_required_columns():
    validate_columns(
        ["txn_id", "timestamp", "device_id", "is_suspicious", "amount"], "dataset_b"
    )


def test_missing_required_column_is_rejected():
    with pytest.raises(DatasetContractError, match="fraud_flag"):
        validate_columns(["txn_id", "timestamp"], "dataset_a")


def test_unknown_dataset_is_rejected():
    with pytest.raises(DatasetContractError, match="Unsupported"):
        validate_columns(["txn_id"], "unknown")
