from sqlalchemy.orm import Session
from models.auth import User
from schemas.auth import UserResponse
from core.security import create_access_token

def get_or_create_user(email: str, username: str, oauth_id: str, db: Session) -> tuple[User, bool]:
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user, False
    
    new_user = User(
        email=email,
        username=username,
        oauth_id=oauth_id,
        oauth_provider="google",
        is_active=True,
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user, True

def authenticate_with_google(google_userinfo: dict, db: Session) -> dict:
    email = google_userinfo.get("email")
    username = google_userinfo.get("name")
    oauth_id = google_userinfo.get("sub")

    if not email or not oauth_id:
        raise ValueError("구글 사용자 정보에 이메일 또는 ID가 없습니다.")
    
    user, created = get_or_create_user(email=email, username=username, oauth_id=oauth_id, db=db)

    token = create_access_token(data={"sub": user.email})

    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": UserResponse.model_validate(user)
    }