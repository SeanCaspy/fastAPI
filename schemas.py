from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str

class UserOut(BaseModel):
    username: str

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner: UserOut

    class Config:
        orm_mode = True
