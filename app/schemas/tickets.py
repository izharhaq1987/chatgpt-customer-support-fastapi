# app/schemas/tickets.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3)
    requester_email: EmailStr
    priority: Optional[str] = "normal"

class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketOut(BaseModel):
    id: int
    subject: str
    description: str
    requester_email: EmailStr
    status: str
    priority: str

    # Pydantic v2 way (replaces inner class Config)
    model_config = ConfigDict(from_attributes=True)
