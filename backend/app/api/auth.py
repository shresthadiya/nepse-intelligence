from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse
)
from app.services.auth_service import (
    register_user,
    authenticate_user
)
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.get(
    "/me",
    response_model=UserResponse
)

def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)

def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = register_user(db, user_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    return user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        credentials.email,
        credentials.password.get_secret_value()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        subject=str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
