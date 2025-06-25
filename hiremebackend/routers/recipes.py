from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from hiremebackend import models, schemas, database_module
from hiremebackend.dependencies import get_current_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/", response_model=schemas.RecipeOut)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_recipe = models.Recipe(**recipe.dict(), owner_id=current_user.id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@router.get("/", response_model=List[schemas.RecipeOut])
def get_all_recipes(db: Session = Depends(database_module.get_db)):
    return db.query(models.Recipe).all()


@router.get("/my", response_model=List[schemas.RecipeOut])
def get_my_recipes(
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Recipe)
        .filter(models.Recipe.owner_id == current_user.id)
        .all()
    )
