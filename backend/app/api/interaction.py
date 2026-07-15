from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.schemas.interaction import (
    InteractionCreate,
    InteractionResponse,
    InteractionUpdate,
)

router = APIRouter(tags=["Interaction"])


@router.post("/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
def create_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db),
):
    hcp = db.query(HCP).filter(HCP.id == payload.hcp_id).first()

    if not hcp:
        raise HTTPException(404, "HCP not found")

    interaction = Interaction(**payload.model_dump())

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


@router.get("/", response_model=List[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
):
    interaction = (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id)
        .first()
    )

    if not interaction:
        raise HTTPException(404, "Interaction not found")

    return interaction


@router.get("/hcp/{hcp_id}", response_model=List[InteractionResponse])
def get_hcp_interactions(
    hcp_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Interaction)
        .filter(Interaction.hcp_id == hcp_id)
        .order_by(Interaction.created_at.desc())
        .all()
    )


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    payload: InteractionUpdate,
    db: Session = Depends(get_db),
):
    interaction = (
        db.query(Interaction)
        .filter(Interaction.id == interaction_id)
        .first()
    )

    if not interaction:
        raise HTTPException(404, "Interaction not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)

    return interaction