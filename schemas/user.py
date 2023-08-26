from pydantic import BaseModel

# schema for input data when getting users
class GetUsers(BaseModel):
    take: int
    orderBy: str

# schema for a user when logged in
class Token(BaseModel):
    access_token: str
    token_type: str
