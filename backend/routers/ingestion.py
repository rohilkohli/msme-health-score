from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db, IngestionRun, FeatureSnapshot, QualityIssue
from models.schemas import (
    IngestionRunRequest,
    IngestionRunResponse,
    FeatureSnapshotResponse,
    QualityIssueResponse,
)
from services.ingestion_pipeline import IngestionPipelineService

router = APIRouter()

@router.post("/run", response_model=IngestionRunResponse)
def trigger_ingestion_run(request: IngestionRunRequest, db: Session = Depends(get_db)):
    service = IngestionPipelineService(db)
    try:
        run = service.run_ingestion(
            msme_id=request.msme_id,
            source=request.source,
            window_start=request.window_start,
            window_end=request.window_end,
            trigger_type=request.trigger_type,
        )
        return run
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during ingestion")

@router.get("/runs/{msme_id}", response_model=List[IngestionRunResponse])
def get_ingestion_runs(msme_id: int, source: str = None, db: Session = Depends(get_db)):
    query = db.query(IngestionRun).filter(IngestionRun.msme_id == msme_id)
    if source:
        query = query.filter(IngestionRun.source == source)
    runs = query.order_by(IngestionRun.started_at.desc()).all()
    return runs

@router.get("/snapshots/{msme_id}", response_model=List[FeatureSnapshotResponse])
def get_feature_snapshots(msme_id: int, db: Session = Depends(get_db)):
    snapshots = (
        db.query(FeatureSnapshot)
        .filter(FeatureSnapshot.msme_id == msme_id)
        .order_by(FeatureSnapshot.created_at.desc())
        .all()
    )
    import json
    result = []
    for s in snapshots:
        result.append({
            "msme_id": s.msme_id,
            "ingestion_run_id": s.ingestion_run_id,
            "snapshot_period": s.snapshot_period,
            "snapshot_granularity": s.snapshot_granularity,
            "metrics": json.loads(s.metrics_json) if s.metrics_json else {},
            "window_3m": json.loads(s.window_3m_json) if s.window_3m_json else {},
            "window_6m": json.loads(s.window_6m_json) if s.window_6m_json else {},
            "window_12m": json.loads(s.window_12m_json) if s.window_12m_json else {},
            "created_at": s.created_at,
        })
    return result

@router.get("/issues/{msme_id}", response_model=List[QualityIssueResponse])
def get_quality_issues(msme_id: int, resolved: bool = None, db: Session = Depends(get_db)):
    query = db.query(QualityIssue).filter(QualityIssue.msme_id == msme_id)
    if resolved is not None:
        query = query.filter(QualityIssue.resolved == resolved)
    issues = query.order_by(QualityIssue.created_at.desc()).all()
    return issues
