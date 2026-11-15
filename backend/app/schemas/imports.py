from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImportRunRead(BaseModel):
    id: int
    source_dataset: str
    filename: str
    file_sha256: str
    status: str
    rows_received: int
    rows_inserted: int
    rows_skipped: int
    error_message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
