from pydantic import BaseModel
from typing import Optional

class SubscriptionCreate(BaseModel):
    name: str
    price: float

class SubscriptionUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]

class SubscriptionOut(BaseModel):
    name: str
    price: str

