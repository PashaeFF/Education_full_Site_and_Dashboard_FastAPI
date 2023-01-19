from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: str