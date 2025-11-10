"""
Aurakode Database Schemas

Define MongoDB collection schemas using Pydantic models.
Each model name maps to a collection with the lowercase class name.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Waitlist(BaseModel):
    email: EmailStr = Field(..., description="Signup email")
    source: Optional[str] = Field(None, description="Optional source tag or ref")
