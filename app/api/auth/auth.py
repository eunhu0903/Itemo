from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from schemas.auth import UserResponse
from datetime import datetime
from core.redis import redis_client
from db.session import get_db
from core.token import get_token_from_header, decode_access_token
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

        profile_image = google_user.get("picture")
        auth_result = authenticate_with_google(google_user, db, profile_image=profile_image)

        return auth_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth 로그인 실패: {str(e)}")
    
@router.get("/me", response_model=UserResponse)
def auth_me(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return user

@router.post("/logout")
def logout(token: str = Depends(get_token_from_header)):
    try:
        payload = decode_access_token(token)
        exp = payload.get("exp")

        if not exp:
            raise HTTPException(status_code=400, detail="토큰 만료 정보 없음")
        
        redis_client.setex(f"bl:{token}", exp - int(datetime.utcnow().timestamp()), "blacklisted")

        return {"message": "로그아웃 되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"로그아웃 실패: {str(e)}")