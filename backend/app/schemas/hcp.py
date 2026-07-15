from pydantic import BaseModel, EmailStr


class HCPBase(BaseModel):
    name: str
    specialization: str
    hospital: str
    city: str
    email: EmailStr


class HCPCreate(HCPBase):
    pass


class HCPUpdate(BaseModel):
    name: str | None = None
    specialization: str | None = None
    hospital: str | None = None
    city: str | None = None
    email: EmailStr | None = None


class HCPResponse(HCPBase):
    id: int

    class Config:
        from_attributes = True