from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from models.database import get_db, User, MSME, DataSource
from models.schemas import DataSourceConnect, DataSourceStatus
from models.enums import DataSourceType
from routers.auth import get_current_user
from utils.helpers import generate_consent_id

router = APIRouter()


@router.post("/connect")
def connect_data_source(data: DataSourceConnect, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == data.msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    existing = db.query(DataSource).filter(
        DataSource.msme_id == data.msme_id,
        DataSource.source_type == data.source_type,
    ).first()

    if existing and existing.status == "completed":
        return {
            "message": f"{data.source_type} already connected",
            "consent_id": existing.consent_id,
            "status": "completed",
        }

    consent_id = generate_consent_id()
    if existing:
        existing.status = "connected"
        existing.consent_id = consent_id
        existing.connected_at = datetime.utcnow()
        existing.last_fetched_at = datetime.utcnow()
    else:
        ds = DataSource(
            msme_id=data.msme_id,
            source_type=data.source_type,
            status="connected",
            consent_id=consent_id,
            connected_at=datetime.utcnow(),
            last_fetched_at=datetime.utcnow(),
        )
        db.add(ds)

    db.commit()
    return {
        "message": f"{data.source_type} connected successfully via Account Aggregator",
        "consent_id": consent_id,
        "status": "connected",
        "data_available": True,
    }


@router.get("/{msme_id}/status", response_model=List[DataSourceStatus])
def get_data_source_status(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    sources = db.query(DataSource).filter(DataSource.msme_id == msme_id).all()
    all_types = ["GST", "UPI", "EPFO", "Account Aggregator"]

    result = []
    connected_types = {s.source_type for s in sources}
    for source_type in all_types:
        if source_type in connected_types:
            s = next(x for x in sources if x.source_type == source_type)
            result.append(DataSourceStatus(
                source_type=s.source_type,
                status=s.status,
                connected_at=s.connected_at,
                last_fetched_at=s.last_fetched_at,
            ))
        else:
            result.append(DataSourceStatus(
                source_type=source_type,
                status="not_connected",
                connected_at=None,
                last_fetched_at=None,
            ))
    return result


@router.post("/{msme_id}/connect-all")
def connect_all_sources(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    all_types = ["GST", "UPI", "EPFO", "Account Aggregator"]
    results = []
    for source_type in all_types:
        existing = db.query(DataSource).filter(
            DataSource.msme_id == msme_id,
            DataSource.source_type == source_type,
        ).first()
        if not existing:
            ds = DataSource(
                msme_id=msme_id,
                source_type=source_type,
                status="completed",
                consent_id=generate_consent_id(),
                connected_at=datetime.utcnow(),
                last_fetched_at=datetime.utcnow(),
            )
            db.add(ds)
            results.append({"source": source_type, "status": "connected"})
        else:
            existing.status = "completed"
            existing.last_fetched_at = datetime.utcnow()
            results.append({"source": source_type, "status": "already_connected"})
    db.commit()
    return {"message": "All data sources connected", "sources": results}
