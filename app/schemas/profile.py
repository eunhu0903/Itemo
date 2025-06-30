from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    status_message: Optional[str] = None

    class Config:
        from_attributes = True