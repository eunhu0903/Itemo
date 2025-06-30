from pydantic import BaseModel

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
