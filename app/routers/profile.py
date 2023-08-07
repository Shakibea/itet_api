from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import Response

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/profile",
    tags=['Profile']
)


@router.get('/', response_model=List[schemas.ProfileResponse])
def all_profile(db: Session = Depends(get_db)):
    allProfile = db.query(models.Profile).all()
    return allProfile


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProfileResponse)
async def create_profile(profile: schemas.ProfileCreateRequest, db: Session = Depends(get_db)):
    new_user = models.Profile(**profile.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.ProfileResponse)
async def get_profile(id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == id).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    return profile
