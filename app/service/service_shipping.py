from fastapi import HTTPException
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

def read_shipping_address(token: str, db: Session):
    user = verify_token(token, db)
    address = db.query(ShippingAddress).filter(ShippingAddress.user_id == user.id).all()
    return address

def read_shipping_address_detail(token: str, address_id: int, db: Session) -> ShippingAddress:
    user = verify_token(token, db)

    address = (
        db.query(ShippingAddress)
        .filter(ShippingAddress.id == address_id, ShippingAddress.user_id == user.id)
        .first()
    )
    if not address:
        raise HTTPException(status_code=404, detail="배송지를 찾을 수 없습니다.")
    return address
