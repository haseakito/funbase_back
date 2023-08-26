from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from prisma import Prisma
from schemas.user import Token
from utils import hash, auth

"""
Router handling the user authentication and authorization
"""
router = APIRouter(
    tags=["Auth"]
)

"""
Function handling logging the user
"""
@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends()):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Query the user with email (note that username defined here is email)
    user = await prisma.user.find_unique(
        where={
            'email': user_cred.username
        }
    )

    # Check if the user is registered
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # Check if the password is correct 
    if not hash.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    # Create an access token for the auth
    access_token = auth.create_access_token(data= { "user_id": user.id })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }