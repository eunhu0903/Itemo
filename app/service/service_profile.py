from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.auth import User
from core.token import verify_token
from core.s3 import upload_fileobj, delete_object, BUCKET_NAME
from urllib.parse import urlparse
import uuid

def get_my_profile(token: str, db: Session) -> User:
    user = verify_token(token, db)
    return user

def update_profile(token: str, profile_data: dict, db: Session) -> User:
    user = verify_token(token, db)
    
    if profile_data.get("username") is not None:
        user.username = profile_data["username"]

    db.commit()
    db.refresh(user)
    return user

def upload_profile_image(user: User, file: UploadFile, db: Session) -> User:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    extension = file.filename.split(".")[-1]
    object_name = f"profile/{uuid.uuid4()}.{extension}"

    image_url = upload_fileobj(file.file, object_name)
    if not image_url:
        raise HTTPException(status_code=500, detail="이미지 업로드 실패")
    
    user.profile_image = image_url
    db.commit()
    db.refresh(user)
    return user

def delete_profile_image(user: User, db: Session) -> User:
    if not user.profile_image:
        raise HTTPException(status_code=400, detail="삭제할 프로필 이미지가 없습니다.")
    
    object_key = urlparse(user.profile_image).path.lstrip('/')
    delete_object(object_name=object_key, bucket_name=BUCKET_NAME)

    user.profile_image = None
    db.commit()
    db.refresh(user)
    return user