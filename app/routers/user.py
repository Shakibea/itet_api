from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import Response

from .. import models, schemas, utils
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/', response_model=List[schemas.UserResponse])
def all_users(db: Session = Depends(get_db)):
    allUsers = db.query(models.User).all()
    return allUsers


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())

    new_user.password = utils.get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, db: Session = Depends(get_db),):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your user not found in Database")
    # my_posts.pop(index)

    # if user.id is not current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="You are not authorized to perform the action!")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
