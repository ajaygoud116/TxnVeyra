from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models import ImportRun
from app.schemas.imports import ImportRunRead
from app.services.dataset_contracts import DatasetContractError
from app.services.ingestion import IngestionError, ingest_csv

router = APIRouter(prefix="/imports", tags=["data imports"])


@router.post("/csv", response_model=ImportRunRead, status_code=201)
async def import_csv(
    source_dataset: str = Query(pattern="^(dataset_a|dataset_b)$"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ImportRunRead:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Only .csv files are accepted")

    content = await file.read(settings.max_upload_size_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Uploaded file exceeds the size limit")

    try:
        run = ingest_csv(
            db,
            source_dataset=source_dataset,
            filename=file.filename,
            content=content,
        )
    except (IngestionError, DatasetContractError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Import failed; see server logs") from exc

    return ImportRunRead.model_validate(run)


@router.get("", response_model=list[ImportRunRead])
def list_imports(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[ImportRunRead]:
    runs = db.scalars(select(ImportRun).order_by(ImportRun.created_at.desc()).limit(limit)).all()
    return [ImportRunRead.model_validate(run) for run in runs]
