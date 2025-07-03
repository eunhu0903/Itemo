import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.product import Product
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