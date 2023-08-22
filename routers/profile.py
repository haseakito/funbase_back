from fastapi import APIRouter, status, HTTPException, Depends
from prisma import Prisma
from models import db
from utils import auth
from schemas import profile

"""
Router handling the user profile
"""
router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)

"""
Function handling getting user's own profile
"""
@router.get('/', status_code=status.HTTP_200_OK, response_model=profile.ProfileOut)
async def get_profile(db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):
    profile = await db.profile.find_unique(
        where={
            'userId': user_id
        }
    )

    return profile

"""
Function handling getting user's profiles by likes
"""
@router.get('/')
async def get_user_profiles(db: Prisma = Depends(db.get_db)):
    profiles = await db.profile.find_many(

    )

    if profiles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"
        )
    return 


"""
Function handling getting the specific user's profile 
"""
@router.get('/{profile_id}', status_code=status.HTTP_200_OK)
async def get_user_profile(profile_id: str, db: Prisma = Depends(db.get_db)):
    profile = await db.profile.find_unique(
        where={
            'userId': profile_id
        }
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return profile


@router.post('/', status_code=status.HTTP_200_OK)
async def update_profile(data: profile.ProfileUpdate, db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):

    # TODO
    if data.profileImage:
        return

    if data.coverImage:
        return

    profile = await db.profile.update(
        where={
            'userId': user_id
        },
        data={
            'bio': data.bio,
            'profileImage': '',
            'coverImage': ''
        }
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )