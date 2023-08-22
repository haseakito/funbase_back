from fastapi import APIRouter, status, HTTPException, Depends
import stripe
from prisma import Prisma
from models import db
from utils import auth
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '../.env')
# Load the environment variables
load_dotenv(env_path)

# Stripe initial configs
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = '2022-08-01; embedded_connect_beta=v1'

"""
Router handling the payment with Stripe APIs
"""
router = APIRouter(
    prefix='/stripe',
    tags=['Stripe']
)

@router.post('/account', status_code=status.HTTP_201_CREATED)
async def create_account(country: str, db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):

    # Call the Stripe API to create a connected account of type express
    account = stripe.Account.create(
        type='express',
        country=country.upper(),
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
        business_type='individual',
    )

    # Call the Stripe API to create an Account Link for that account's ID
    stripe.AccountLink.create(
        account=account.stripe_id,
        refresh_url='',
        return_url='',
        type='account_onboarding',
        collect='eventually_due'
    )

    # Store the account Id in the database
    await db.stripeaccount.create(
        data={
            'stripeAccountId': account.stripe_id,
            'userId': user_id,
        }
    )

@router.post('/account_session', status_code=status.HTTP_200_OK)
async def create_account_session():
    try:
        account_session = stripe.AccountSession.create(
            account=os.getenv("STRIPE_CONNECTED_ID")
        )

        return {'client_secret': account_session.client_secret }
    
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account session: ', e)
        return e
    
"""
Function handling subscribing to a plan
"""
@router.post('/{plan_id}', status_code=status.HTTP_200_OK)
async def create_checkout_session(plan_id: str, db: Prisma = Depends(db.get_db), user_id: str = Depends(auth.get_current_user)):

    # Query the subscription plan with plan_id
    plan = await db.subscriptionplan.find_unique(
        where={
            'id': plan_id
        }
    )

    # Call the Stripe checkout session api
    checkout_session = stripe.checkout.Session.create(
        customer=user_id,
        payment_method_type=['card'],
        mode='subscription',
        line_items=[
            {
                'quantity': 1,
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': plan.price,
                    'product_data': {
                        'name': plan.name,
                    },
                    'recurring': 'month'
                },
            },
        ],
        subscription_data={
            'application_fee_percent': 10,
            'transfer_data': {
                'destination': plan.authorId
            },
            'trial_period_days': 30
        },
        success_url="",
        cancel_url=""
    )

    # Create the subscription
    await db.subscription.create(
        data={
            'subscriberId': user_id,
            'planId': plan_id,
        }
    )

    