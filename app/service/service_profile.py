from sqlalchemy.orm import Session
from models.auth import User
from core.token import verify_token

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
