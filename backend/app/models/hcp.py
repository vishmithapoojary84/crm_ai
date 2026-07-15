from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)

    specialization = Column(String, index=True)

    hospital = Column(String, index=True)

    city = Column(String)

    email = Column(String, unique=True, index=True)

    interactions = relationship(
        "Interaction",
        back_populates="hcp",
        cascade="all, delete-orphan"
    )