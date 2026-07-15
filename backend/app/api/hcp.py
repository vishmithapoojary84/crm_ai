from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPResponse

router = APIRouter(tags=["HCP"])


@router.post("/", response_model=HCPResponse, status_code=status.HTTP_201_CREATED)
def create_hcp(payload: HCPCreate, db: Session = Depends(get_db)):
    existing = db.query(HCP).filter(HCP.email == payload.email).first()

    if existing:
        raise HTTPException(400, "HCP with this email already exists")

    hcp = HCP(**payload.model_dump())

    db.add(hcp)
    db.commit()
    db.refresh(hcp)

    return hcp


@router.get("/", response_model=List[HCPResponse])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()

    if not hcp:
        raise HTTPException(404, "HCP not found")

    return hcp


@router.get("/search/", response_model=List[HCPResponse])
def search_hcp(
    query: str = Query(...),
    db: Session = Depends(get_db),
):
    return (
        db.query(HCP)
        .filter(HCP.name.ilike(f"%{query}%"))
        .all()
    )


@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(
    hcp_id: int,
    payload: HCPUpdate,
    db: Session = Depends(get_db),
):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()

    if not hcp:
        raise HTTPException(404, "HCP not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(hcp, key, value)

    db.commit()
    db.refresh(hcp)

    return hcp