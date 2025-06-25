from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ===== USER SCHEMAS =====

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ===== DELIVERY SCHEMAS =====
class DeliveryBase(BaseModel):
    item_name: str
    quantity: int
    pickup_address: str
    dropoff_address: str
    instructions: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryRead(DeliveryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True




# ===== COUPON SCHEMAS =====
class CouponBase(BaseModel):
    code: str
    discount: float
    expiry: str
    description: Optional[str] = None

class CouponCreate(CouponBase):
    pass

class CouponRead(CouponBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class CouponOut(CouponRead):
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
        
class RecipeCreate(BaseModel):
    title: str
    video_url: str
    description: str | None = None

class RecipeOut(RecipeCreate):
    id: int
    owner_id: int

class Config:
    orm_mode = True
        
class NotificationCreate(BaseModel):
    message: str

# For returning a notification to the frontend
class NotificationOut(NotificationCreate):
    id: int
    user_id: int
    is_read: bool
    timestamp: datetime

    class Config:
        orm_mode = True