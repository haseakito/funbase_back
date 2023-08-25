from pydantic import BaseModel
from prisma.models import User

# user response schema
User.create_partial('UserOut', exclude_relational_fields=True, exclude={{ 'password', 'emailVerified' }})

# get a user response schema
User.create_partial('UserGet', exclude={{ 'password' }})

# user login schema
User.create_partial('UserLogin', include={{ 'email', 'password' }})

# user create schema
User.create_partial('UserCreate', include={{ 'username', 'email', 'password' }})

# reset password schema
User.create_partial('ResetPassword', include={{ 'email', 'password' }})

# schema for input data when getting users
class GetUsers(BaseModel):
    take: int
    orderBy: str

# schema for a user when logged in
class Token(BaseModel):
    access_token: str
    token_type: str
