from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(
        User.username == username
    ).first()

def register_user(db: Session, user_data: UserCreate):
    if get_user_by_email(db, user_data.email):
        return None

    if get_user_by_username(db, user_data.username):
        return None

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="viewer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
