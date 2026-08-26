from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
