from fastapi import APIRouter, status, HTTPException, Response, Depends
from prisma import Prisma
from prisma.partials import UserGet, UserOut, UserCreate
from models import db
from utils import hash, auth
from schemas import user

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
async def get_users(condition: user.GetUsers, db: Prisma = Depends(db.get_db)):
    # Query users with custom parameters
    users = await db.user.find_many(
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
async def get_user(user_id: str, db: Prisma = Depends(db.get_db)):
    user = db.user.find_unique(
        where={
            'id': {user_id}
        }
    )

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

"""
Function handling creating the user with email and password
"""
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Prisma = Depends(db.get_db)):
    # Query the user by email to avoid registering the same email
    db_user = db.user.find_unique(
        where={
            'email': user.email
        }
    )
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered!")
    
    # Create user
    await db.user.create(
        data={
            'username': user.username,
            'email': user.email,
            'password': hash.hash_password(user.password)
        }
    )

    #TODO: Send email verification

    return 

"""
Function handling resetting the password
"""
@router.put('/reset', status_code=status.HTTP_200_OK)
async def reset_password(user: user.ResetPassword , db: Prisma = Depends(db.get_db)):
    # Query the user by email
    user = await db.user.find_unique(
        where={
            'email': user.email
        }
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found!')

    # Update the password
    await db.user.update(
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
async def delete_user(db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):
    # Query the user with id
    user = await db.user.delete(
        where={
            'id': user_id
        }
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)