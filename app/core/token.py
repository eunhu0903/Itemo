from fastapi import HTTPException, status, Header
from core.redis import redis_client
from datetime import datetime
from sqlalchemy.orm import Session
from models.auth import User
from core.security import decode_access_token

def get_token_from_header(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 토큰이 없거나 잘못되었습니다.")
    return authorization[7:]

def verify_token(token: str, db: Session) -> User:
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 디코딩에 실패했습니다.")

    email: str = payload.get("sub")
    if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰에 이메일 정보가 없습니다.")

    if redis_client.get(f"bl:{token}") == "blacklisted":
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="존재하지 않는 사용자입니다.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="정지된 계정입니다.")

    expiration: int = payload.get("exp")
    if expiration and expiration < int(datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었습니다.")

    return user
