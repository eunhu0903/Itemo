from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True