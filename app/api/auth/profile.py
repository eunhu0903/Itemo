from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from schemas.profile import ProfileResponse, ProfileUpdateRequest
from core.token import get_token_from_header, verify_token
from db.session import get_db
from service.service_profile import get_my_profile, update_profile, upload_profile_image, delete_profile_image

router = APIRouter(tags=["Profile"])

@router.get("/profile", response_model=ProfileResponse)
def get_profile(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = get_my_profile(token, db)
    return user

@router.patch("/profile", response_model=ProfileResponse)
def patch_profile(profile_update: ProfileUpdateRequest, token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = update_profile(token, profile_update.dict(exclude_unset=True), db)
    return user

@router.post("/profile/image", response_model=ProfileResponse)
async def post_upload_profile_image(
    file: UploadFile = File(...),
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = verify_token(token, db)
    updated_user = upload_profile_image(user, file, db)
    return updated_user

@router.delete("/profile/image", response_model=ProfileResponse)
def delete_profile_image_api(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = verify_token(token, db)

    if not user.profile_image:
        raise HTTPException(status_code=400, detail="Google 이미지 상태에서는 삭제할 수 없습니다.")
    
    updated_user = delete_profile_image(user, db)
    return updated_user