from pydantic import BaseModel
from typing import Optional

class ProfileUpdate(BaseModel):
    bio: Optional[str]
    profileImage: Optional[str]
    coverImage: Optional[str]

class ProfileOut(BaseModel):
    profileImage: str
    coverImage: str