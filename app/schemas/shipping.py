from pydantic import BaseModel
from typing import Optional

class ShippingAddressesCreate(BaseModel):
    recipient: str
    phone_number: str
    address: str
    detail_address: str | None = None
    postal_code: str
    
class ShippingAddressesResponse(BaseModel):
    id: int
    recipient: str
    phone_number: str
    address: str
    detail_address: str
    postal_code: str

    class Config:
        from_attributes = True

class ShippingAddressesUpdate(BaseModel):
    recipient: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    detail_address: Optional[str] = None
    postal_code: Optional[str] = None