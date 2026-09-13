from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactOut(ContactCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectCreate(BaseModel):
    title: str
    description: str
    tech: str
    demo_url: str | None = None
    image: str | None = None

class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
