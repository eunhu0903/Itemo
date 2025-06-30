from pydantic import BaseModel, Field

class ShippingAddressesCreate(BaseModel):
    recipient: str
    phone_number: str
    address: str
    detail_address: str | None = None
    postal_code: str
    