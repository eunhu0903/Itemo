from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    profile_image: Optional[str]

    class Config:
        from_attributes = True

class ProfileUpdateRequest(BaseModel):
    username: Optional[str] = None