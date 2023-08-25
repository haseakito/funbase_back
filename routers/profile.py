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
Function updating the user's profile
"""
@router.post('/', status_code=status.HTTP_200_OK)
async def update_profile(data: profile.ProfileUpdate, db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):

    # TODO: Add AWS S3 sdk to upload image
    if data.profileImage:
        return

    # TODO: Add AWS S3 sdk to upload image
    if data.coverImage:
        return

    # Update the profile
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