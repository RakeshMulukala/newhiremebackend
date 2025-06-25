from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from hiremebackend import models, schemas, database_module
from hiremebackend.auth import get_current_user

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/", response_model=schemas.CouponRead)
def create_coupon(
    coupon: schemas.CouponCreate,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_coupon = models.Coupon(**coupon.dict(), owner_id=current_user.id)
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return new_coupon

@router.get("/", response_model=List[schemas.CouponRead])
def get_user_coupons(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Coupon)
        .filter(models.Coupon.owner_id == current_user.id)
        .order_by(models.Coupon.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
