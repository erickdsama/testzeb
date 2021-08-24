from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str
    role_id: int
    photo: Optional[str]

    class Config:
        orm_mode = True
