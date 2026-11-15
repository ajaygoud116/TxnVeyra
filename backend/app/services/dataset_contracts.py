from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetContract:
    name: str
    required_columns: frozenset[str]
    timestamp_column: str = "timestamp"
    record_id_column: str = "txn_id"


CONTRACTS = {
    "dataset_a": DatasetContract(
        name="dataset_a",
        required_columns=frozenset({"txn_id", "timestamp", "fraud_flag"}),
    ),
    "dataset_b": DatasetContract(
        name="dataset_b",
        required_columns=frozenset({"txn_id", "timestamp", "device_id", "is_suspicious"}),
    ),
}


class DatasetContractError(ValueError):
    pass


def validate_columns(columns: list[str], source_dataset: str) -> None:
    if source_dataset not in CONTRACTS:
        raise DatasetContractError(f"Unsupported source_dataset: {source_dataset}")

    contract = CONTRACTS[source_dataset]
    missing = sorted(contract.required_columns - set(columns))
    if missing:
        raise DatasetContractError(
            f"{source_dataset} is missing required columns: {', '.join(missing)}"
        )
