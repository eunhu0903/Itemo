from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.profile import ProfileResponse
from core.token import get_token_from_header
from db.session import get_db
from service.service_profile import get_my_profile

router = APIRouter(tags=["Profile"])

@router.get("/profile", response_model=ProfileResponse)
def read_my_profile(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = get_my_profile(token, db)
    return user