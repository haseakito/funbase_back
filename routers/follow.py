from fastapi import APIRouter, status, HTTPException, Depends
from prisma import Prisma
from models import db
from utils import auth

"""
Router handling the follow
"""
router = APIRouter(
    prefix='/follow',
    tags=['Follow']
)

"""
Function handlig getting the users that current user are followed by
"""
@router.get('/followers/{user_id}', status_code=status.HTTP_200_OK)
async def get_followers(user_id: str, db: Prisma = Depends(db.get_db)):
    user = await db.user.find_unique(
        where={
            'id': user_id,
        },
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user.follower

"""
Function handlig getting the users that current user follows
"""
@router.get('/followings/{user_id}', status_code=status.HTTP_200_OK)
async def get_followings(user_id: str, db: Prisma = Depends(db.get_db)):
    user = await db.user.find_unique(
        where={
            'id': user_id
        }
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found'
        )
    
    return user.following

"""
Function handling that current user follows a user 
"""
@router.post('/{following_user_id}', status_code=status.HTTP_200_OK)
async def follow(following_user_id: str,
                 db: Prisma = Depends(db.get_db),
                 user_id: str = Depends(auth.get_current_user)):
    
    # Query the current user with user with user_id
    user = await db.user.find_unique(
        where={
            'id': following_user_id
        }
    )

    # Check if the user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    
    # Check if the current user has already followed the user with following_user_id
    if following_user_id in user.follower:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Already Followed the User"
        )
    
    # Create the follow data
    await db.follow.create(
        data={
            'followingId': user_id,
            'followerId': following_user_id
        }
    )

"""
Function handling that current user unfollows a user 
"""
@router.delete('/{following_user_id}', status_code=status.HTTP_200_OK)
async def unfollow(following_user_id: str,
                   db: Prisma = Depends(db.get_db),
                   user_id: str = Depends(auth.get_current_user)):
    
    # Query the user with following_user_id
    user = await db.user.find_unique(
        where={
            'id': following_user_id
        }
    )

    # Check if the user with following_user_id exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found'
        )
    
    # Check if the current user has followed the user with following_user_id 
    if not following_user_id in user.following:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='User has not followed this user'
        )
    
    # Delete the follow data
    await db.follow.delete(
        where= {
            {
                'followingId': user_id,
                'followerId': following_user_id
            }
        }
    )