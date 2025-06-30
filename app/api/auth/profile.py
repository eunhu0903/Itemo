from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.profile import ProfileResponse, ProfileUpdateRequest
from core.token import get_token_from_header
from db.session import get_db
from service.service_profile import get_my_profile, update_profile

router = APIRouter(tags=["Profile"])

@router.get("/profile", response_model=ProfileResponse)
def get_profile(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = get_my_profile(token, db)
    return user
@router.patch("/profile", response_model=ProfileResponse)
def patch_profile(profile_update: ProfileUpdateRequest, token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = update_profile(token, profile_update.dict(exclude_unset=True), db)
    return user