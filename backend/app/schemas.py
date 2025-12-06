from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# Schemas Users
class UserPost(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
