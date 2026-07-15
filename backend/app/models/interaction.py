from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Date,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(
        Integer,
        ForeignKey("hcps.id"),
        nullable=False,
        index=True
    )

    meeting_type = Column(String)

    discussion = Column(Text)

    summary = Column(Text)

    follow_up_date = Column(Date)

    status = Column(
        String,
        default="Pending",
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    hcp = relationship(
        "HCP",
        back_populates="interactions"
    )