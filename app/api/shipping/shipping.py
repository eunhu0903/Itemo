from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.shipping import ShippingAddressesCreate, ShippingAddressesResponse
from db.session import get_db
from core.token import get_token_from_header
from typing import List
from service.service_shipping import create_shipping_address, read_shipping_address

router = APIRouter(tags=["Shipping-addresses"])

@router.post("/shipping-addresses")
def post_shipping_addresses(
    address_data: ShippingAddressesCreate,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    new_address = create_shipping_address(token, address_data, db)
    return {"message": "배송지가 등록되었습니다.", "shipping_address_id": new_address.id}

@router.get("/shipping-addresses", response_model=List[ShippingAddressesResponse])
def get_shipping_addresses(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    address = read_shipping_address(token, db)
    return address