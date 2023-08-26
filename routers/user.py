from fastapi import APIRouter, status, HTTPException, Response, Depends
from prisma import Prisma
from prisma.partials import UserOut, UserGet, UserCreate, ResetPassword
from utils import hash, auth, email
from schemas.user import GetUsers, EmailSchema, Token

"""
Router handling the user operation api
"""
router = APIRouter(
    prefix='/user',
    tags=['User']
)

"""
Function handling getting users by custom parameters
"""
@router.get('/', response_model=list[UserOut])
async def get_users(condition: GetUsers):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Query users with custom parameters
    users = await prisma.user.find_many(
        take=condition.take,
        order={
            condition.orderBy: 'desc'
        }
    )
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users Not Found!')

    return users

"""
Function handling getting the user with id
"""
@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserGet)
async def get_user(user_id: str):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Query the user with user id
    user = prisma.user.find_unique(
        where={
            'id': user_id
        }
    )

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

"""
Function handling creating the user with email and password
"""
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(user: UserCreate):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()
    
    # Query the user by email to avoid registering the same email        
    db_user = await prisma.user.find_unique(
        where={
            'email': user.email
        }
    )
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered!")

    # Create user
    user_res = await prisma.user.create(
        data={
            'username': user.username,
            'email': user.email,
            'password': hash.hash_password(user.password)
        }
    )

    # Send email to user email
    await email.send_email(
        EmailSchema(
            email=[user.email],
            body={"username": user.username}
        )
    )

    return {
        "access_token": auth.create_access_token({'user_id' : user_res.id}),
        "token_type": "bearer"
    }

"""
Function handling verifying the email
"""
@router.put('/verify', status_code=status.HTTP_200_OK)
async def verify_email(user_id: str = Depends(auth.get_current_user)):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()
    
    # Query the user by user id
    user = await prisma.user.update(
        where={
            'id': user_id
        },
        data={
            'emailVerified': True
        }
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found!')
    

"""
Function handling resetting the password
"""
@router.put('/reset', status_code=status.HTTP_200_OK)
async def reset_password(user: ResetPassword ):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Query the user by email
    user = await prisma.user.find_unique(
        where={
            'email': user.email
        }
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found!')

    # Update the password
    await prisma.user.update(
        where={
            'email': user.email
        },
        data={
            'password': hash.hash_password(user.password)
        }
    )

"""
Function handling deleting the user
"""
@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_user(user_id: str = Depends(auth.get_current_user)):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Query the user with id
    user = await prisma.user.delete(
        where={
            'id': user_id
        }
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)