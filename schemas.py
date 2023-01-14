from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi_pagination.bases import RawParams, AbstractParams

class Education(BaseModel):
    name: str

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: str
    password: str

class Users(BaseModel):
    name_surname: str
    age: int
    city: str
    phone: str
    education: str
    certificate_points: str
    about: str
    select_university_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
        
from datetime import datetime
class News(BaseModel):
    id: int = Field(...)
    news_title: str = Field(...)
    select_category_id: int = Field(...)
    created_at: datetime = Field(...)

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.total_items,
            offset=self.total_items * self.return_per_page,
        )

    class Config:
        orm_mode = True
