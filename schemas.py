from pydantic import BaseModel
from typing import Optional, List


class BlogRequest(BaseModel):
    title: str
    body: str
    user_id: int
    # published: Optional[bool]

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    name: str
    email: str
    password: str


class UserReturn(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[BlogRequest] = None

    class Config:
        orm_mode = True


class UserReturn1(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserReturn2(BaseModel):
    status: int = 200
    detail: str = "Success"
    data: List[UserReturn]

    class Config:
        orm_mode = True


class BlogReturn(BaseModel):
    id: int
    title: str
    body: str
    created_by: UserReturn1 = None

    class Config:
        orm_mode = True

class BlogReturnMain(BaseModel):
    status: int
    detail: str
    data: BlogReturn = None

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None