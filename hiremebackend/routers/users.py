from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hiremebackend import models, schemas
from hiremebackend.database_module import get_db
from hiremebackend.auth import get_password_hash
from hiremebackend.auth import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserBase)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(email=user.email, username=user.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=schemas.UserBase)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
