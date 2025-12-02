from typing import List

from pydantic import BaseModel, EmailStr

from app.models import FoodTypeModel, UserRole


class Message(BaseModel):
    message: str


# Schemas Users
class UserPost(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    senha: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


# Schemas Stores
class StorePost:
    name: str
    address: str
    partner_id: int
    food_types: List[FoodTypeModel]
