from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class InteractionBase(BaseModel):
    hcp_id: int
    meeting_type: str
    discussion: str
    summary: Optional[str] = None
    follow_up_date: Optional[date] = None
    status: str = "Pending"


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    meeting_type: Optional[str] = None
    discussion: Optional[str] = None
    summary: Optional[str] = None
    follow_up_date: Optional[date] = None
    status: Optional[str] = None


class InteractionResponse(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True