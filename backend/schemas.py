from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Waitlist(BaseModel):
    email: EmailStr = Field(..., description="Email to join the waitlist")
    source: Optional[str] = Field(None, description="Optional source or ref tag")
