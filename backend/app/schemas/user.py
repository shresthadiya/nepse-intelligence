from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    SecretStr
)

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: SecretStr = Field(
        min_length=8,
        max_length=128
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
