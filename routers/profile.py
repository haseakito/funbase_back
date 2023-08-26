from fastapi import APIRouter, status, HTTPException, Depends
from prisma import Prisma
from prisma.partials import UpdateBio, UpdateProfile, UpdateCover
from utils import auth


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
@router.post('/image', status_code=status.HTTP_200_OK)
async def update_profile(data: UpdateProfile, user_id: str = Depends(auth.get_current_user)):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # TODO: Add AWS S3 sdk to upload image
    if data.profileImage:
        return

    # Update the profile image for the user by user id
    profile = await prisma.profile.update(
        where={
            'userId': user_id
        },
        data={            
            'profileImage': '',            
        }
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
@router.put('/bio', status_code=status.HTTP_200_OK)
async def update_bio(data: UpdateBio, user_id: str = Depends(auth.get_current_user)):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()

    # Update the profile bio for the user by user id
    profile = await prisma.profile.update(
        where={
            'userId': user_id
        },
        data={
            'bio': data.bio
        }
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put('/', status_code=status.HTTP_200_OK)
async def update_cover(data: UpdateCover, user_id: str = Depends(auth.get_current_user)):
    # Connect to database
    prisma = Prisma()
    await prisma.connect()
    
    # TODO: Add AWS S3 sdk to upload image
    if data.coverImage:
        return

    # Update the profile coverImage for the user by user id
    profile = await prisma.profile.update(
        where={
            'userId': user_id
        },
        data={
            'coverImage': ''
        }
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )