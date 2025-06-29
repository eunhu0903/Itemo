from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from schemas.auth import UserResponse
from db.session import get_db
from core.token import get_token_from_header
from core.oauth import get_google_auth_url, exchange_code_for_token, get_google_userinfo
from service.service_auth import authenticate_with_google, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login/google")
async def login_google():
    auth_url = get_google_auth_url()
    return RedirectResponse(auth_url)

@router.get("/callback/google")
async def callback_google(code: str, db: Session = Depends(get_db)):
    try:
        token_response = await exchange_code_for_token(code)
        access_token = token_response.get("access_token")

        google_user = await get_google_userinfo(access_token)

        auth_result = authenticate_with_google(google_user, db)

        return auth_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth 로그인 실패: {str(e)}")
    
@router.get("/me", response_model=UserResponse)
def auth_me(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return user