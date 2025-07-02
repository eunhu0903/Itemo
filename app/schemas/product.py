from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    product_image: Optional[str]

    class Config:
        from_attributes = True
