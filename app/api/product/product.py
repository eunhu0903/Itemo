from fastapi import APIRouter, Depends, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from core.token import verify_token, get_token_from_header
from db.session import get_db
from typing import List
from schemas.product import ProductResponse
from service.service_product import create_product, read_all_product, read_product, update_product, delete_product, read_my_product

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

@router.get("/products/me", response_model=List[ProductResponse])
def get_my_product(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    product = read_my_product(user, db)
    return product

@router.get("/products/{products_id}", response_model=ProductResponse)
def get_product(products_id: int, db: Session = Depends(get_db)):
    product = read_product(products_id, db)
    return product

@router.put("/products/{products_id}", response_model=ProductResponse)
def put_product(
    products_id: int = Path(...), 
    name: str = Form(...), 
    description: str = Form(...), 
    price: int = Form(...), 
    image: UploadFile = File(...), 
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = verify_token(token, db)
    product = update_product(products_id, name, description, price, image, user, db)
    return product

@router.delete("/products/{products_id}")
def delete_product_api(
    products_id: int,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = verify_token(token, db)
    delete_product(products_id, user, db)
    return {"message": "상품이 성공적으로 삭제되었습니다."}
