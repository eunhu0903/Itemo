from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.shipping import ShippingAddressesCreate, ShippingAddressesResponse, ShippingAddressesUpdate
from db.session import get_db
from core.token import get_token_from_header
from typing import List
from service.service_shipping import create_shipping_address, read_shipping_address, read_shipping_address_detail, update_shipping_address, delete_shipping_address, set_default_shipping_address

router = APIRouter(tags=["Shipping-addresses"])

@router.post("/shipping-addresses")
def post_shipping_address(
    address_data: ShippingAddressesCreate,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    new_address = create_shipping_address(token, address_data, db)
    return {"message": "배송지가 등록되었습니다.", "shipping_address_id": new_address.id}

@router.get("/shipping-addresses", response_model=List[ShippingAddressesResponse])
def get_shipping_address(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    address = read_shipping_address(token, db)
    return address

@router.get("/shipping-addresses/{address_id}", response_model=ShippingAddressesResponse)
def get_shipping_address_detail(
    address_id: int, 
    token: str = Depends(get_token_from_header), 
    db: Session = Depends(get_db)
):
    address = read_shipping_address_detail(token, address_id, db)
    return address

@router.patch("/shipping-addresses/{address_id}", response_model=ShippingAddressesResponse)
def patch_shipping_address(
    address_id: int,
    address_data: ShippingAddressesUpdate,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    address = update_shipping_address(token, address_id, address_data, db)
    return address

@router.patch("/shipping-addresses/{address_id}/default", response_model=ShippingAddressesResponse)
def patch_default_shipping_address(
    address_id: int, 
    token: str = Depends(get_token_from_header), 
    db: Session = Depends(get_db)
):
    updated = set_default_shipping_address(token, address_id, db)
    return updated

@router.delete("/shipping-addresses/{address_id}")
def delete_shipping_address_api(
    address_id: int,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    delete_shipping_address(token, address_id, db)
    return {"message": "배송지가 삭제되었습니다."}