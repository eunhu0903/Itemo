import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.product import Product
from schemas.product import ProductUpdate
from models.auth import User
from core.s3 import upload_fileobj


def create_product(name: str, description: str, price: int, image: UploadFile, user: User, db: Session) -> Product:
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    extension = image.filename.split(".")[-1]
    object_name = f"product/{uuid.uuid4()}.{extension}"

    product_image = upload_fileobj(image.file, object_name)
    if not product_image:
        raise HTTPException(status_code=500, detail="이미지 업로드 실패")
    
    product = Product(
        name=name,
        description=description,
        price=price,
        product_image=product_image,
        seller_id=user.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def read_all_product(db: Session) -> List[Product]:
    product = db.query(Product).all()
    return product

def read_product(products_id: int, db: Session) -> Product:
    product = db.query(Product).filter(Product.id == products_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")
    return product

def update_product(products_id: int, name: str, description: str, price: float, image: UploadFile | None, seller_id: User, db: Session):
    product = db.query(Product).filter(Product.id == products_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")
    if product.seller_id != seller_id.id:
        raise HTTPException(status_code=403, detail="상품 수정 권한이 없습니다.")
    
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
        extension = image.filename.split(".")[-1]
        object_name = f"product/{uuid.uuid4()}.{extension}"

        image_url = upload_fileobj(image.file, object_name)
        if not image_url:
            raise HTTPException(status_code=500, detail="이미지 업로드 실패")
        product.product_image = image_url
    
    product.name = name
    product.description = description
    product.price = price
    
    db.commit()
    db.refresh(product)
    return product

def delete_product(products_id, seller_id: User, db: Session):
    product = db.query(Product).filter(Product.id == products_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")
    if product.seller_id != seller_id.id:
        raise HTTPException(status_code=403, detail="상품 삭제 권한이 없습니다.")
    
    db.delete(product)
    db.commit()