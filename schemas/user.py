from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any 

# schema for input data when getting users
class GetUsers(BaseModel):
    take: int
    orderBy: str

class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]

# schema for a user when logged in
class Token(BaseModel):
    access_token: str
    token_type: str
