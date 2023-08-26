from fastapi import APIRouter, status, HTTPException, Depends
from prisma import Prisma
from models import db
from schemas import subscription
from utils import auth

"""
Router handling subscription operation
"""
router = APIRouter(
    prefix='/plan',
    tags=['Plan']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_plan(
    data: subscription.SubscriptionCreate,
    db: Prisma = Depends(db.get_db),
    user_id: str = Depends(auth.get_current_user)):

    # Create the subscription plan
    await db.subscriptionplan.create(
        data={
            'authorId': user_id,
            'name': data.name,
            'price': data.price,
        }
    )

"""
Function handling getting the plans that the user has
"""
@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=subscription.SubscriptionOut)
async def get_plans(user_id: str, db: Prisma = Depends(db.get_db)):
    # Query the subscription plans for a user
    user = await db.user.find_unique(
        where={
            'id': user_id
        }
    )

    # Check if the user exists 
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    
    return user.plan

@router.put('/{plan_id}', status_code=status.HTTP_200_OK)
async def update_plan(
    plan_id: str,
    data: subscription.SubscriptionUpdate,
    db: Prisma = Depends(db.get_db),
    user_id: str = Depends(auth.get_current_user)):
    # Query the subscription plan
    plan = await db.subscriptionplan.find_unique(
        where={
            'id': plan_id
        }
    )

    # Check if the user is the owner of the plan
    if plan.authorId is not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    # Update the subscription plan
    result = await db.subscriptionplan.update(
        where={
            'id': plan_id
        },
        data={
            'name': data.name,
            'price': data.price,
        }
    )

@router.delete('/{plan_id}', status_code=status.HTTP_200_OK)
async def delete_plan(plan_id: str, db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):
    # Query the subscription plan
    plan = await db.subscriptionplan.find_unique(
        where={
            'id': plan_id
        }
    )

    # Check if the user is the owner of the plan
    if plan.authorId is not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    # Delete the subscription plan
    await db.subscriptionplan.delete(
        where={
            'id': plan_id
        }
    )
