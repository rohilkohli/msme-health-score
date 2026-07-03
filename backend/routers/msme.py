from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.database import get_db, User, MSME
from models.schemas import MSMERegister, MSMEProfile
from routers.auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=MSMEProfile)
def register_msme(data: MSMERegister, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(MSME).filter(MSME.gstin == data.gstin).first()
    if existing:
        raise HTTPException(status_code=400, detail="MSME with this GSTIN already registered")

    msme = MSME(
        user_id=current_user.id,
        business_name=data.business_name,
        gstin=data.gstin,
        pan=data.pan,
        udyam_number=data.udyam_number,
        business_type=data.business_type,
        industry=data.industry,
        city=data.city,
        state=data.state,
        pincode=data.pincode,
        annual_turnover=data.annual_turnover,
        employee_count=data.employee_count,
        year_established=data.year_established,
        upi_id=data.upi_id,
        epfo_establishment_id=data.epfo_establishment_id,
        bank_account_number=data.bank_account_number,
        ifsc_code=data.ifsc_code,
    )
    db.add(msme)
    db.commit()
    db.refresh(msme)
    return msme


@router.get("/list", response_model=List[MSMEProfile])
def list_msmes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msmes = db.query(MSME).filter(MSME.user_id == current_user.id).all()
    return msmes


@router.get("/{msme_id}", response_model=MSMEProfile)
def get_msme(msme_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")
    return msme
