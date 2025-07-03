from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from core.token import verify_token, get_token_from_header
from db.session import get_db
from typing import List
from schemas.product import ProductResponse
from service.service_product import create_product, read_all_product

router = APIRouter(tags=["Product"])

@router.post("/products", response_model=ProductResponse)
def post_product(
    name: str = Form(...), 
    description: str = Form(...), 
    price: int = Form(...), 
    image: UploadFile = File(...), 
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = verify_token(token, db)
    product = create_product(name, description, price, image, user, db)
    return product

@router.get("/products", response_model=List[ProductResponse])
def get_all_product(db: Session = Depends(get_db)):
    product = read_all_product(db)
    return product