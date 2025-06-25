# hiremebackend/routers/notifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from hiremebackend import models, schemas, database_module
from hiremebackend.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=schemas.NotificationOut)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_notification = models.Notification(
        **notification.dict(),
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


@router.get("/", response_model=List[schemas.NotificationOut])
def get_my_notifications(
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == current_user.id)
        .order_by(models.Notification.timestamp.desc())
        .all()
    )


@router.patch("/{notification_id}/read", response_model=schemas.NotificationOut)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

def create_notification_for_user(db: Session, user_id: int, message: str):
    notification = models.Notification(
        user_id=user_id,
        message=message,
        is_read=False,
        timestamp=datetime.utcnow()
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification