from sqlalchemy.orm import Session
from models.auth import User
from core.token import verify_token

def get_my_profile(token: str, db: Session) -> User:
    user = verify_token(token, db)
    return user