from pydantic import BaseModel, EmailStr

from app.enums import UserRole


class Message(BaseModel):
    message: str


# Schemas Users
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    senha: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
