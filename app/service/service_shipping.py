from sqlalchemy.orm import Session 
from schemas.shipping import ShippingAddressesCreate
from models.shipping import ShippingAddress
from core.token import verify_token

def create_shipping_address(token: str, address_data: ShippingAddressesCreate, db: Session) -> ShippingAddress:
    user = verify_token(token, db)

    new_address = ShippingAddress(
        user_id=user.id,
        recipient=address_data.recipient,
        phone_number=address_data.phone_number,
        address=address_data.address,
        detail_address=address_data.detail_address,
        postal_code=address_data.postal_code
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address