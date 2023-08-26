from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta

env_path = os.path.join(os.path.dirname(__file__), '../.env')
# Load the environment variables
load_dotenv(env_path)

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl='login'
)

# JWT encode configs
SECRET_KEY= os.getenv("AUTH_SECRET")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE = 7

"""
Function handling creating the access JWT token
"""
def create_access_token(data: dict):
    to_encode = data.copy()

    # Set the token expiry period
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

"""
Function handling verifying the token
"""
def verify_access_token(token: str, credential_exception):
    try:
        # Decode the token 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credential_exception

    except JWTError:
        raise credential_exception
    
    return user_id
    
"""
Function getting the current logged in user
"""
def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credential_exception)