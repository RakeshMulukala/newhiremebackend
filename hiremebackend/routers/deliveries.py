from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hiremebackend import models, schemas
from hiremebackend.database_module import get_db
from hiremebackend.auth import get_current_user

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

@router.post("/", response_model=schemas.DeliveryBase)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_delivery = models.Delivery(**delivery.dict(), user_id=current_user.id)
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery

@router.get("/", response_model=list[schemas.DeliveryBase])
def list_deliveries(db: Session = Depends(get_db)):
    return db.query(models.Delivery).all()

@router.patch("/{delivery_id}/accept")
def accept_delivery(delivery_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if delivery.status != "Pending":
        raise HTTPException(status_code=400, detail="Delivery already accepted")
    delivery.status = "Accepted"
    db.commit()
    return {"message": "Delivery accepted"}
