from typing import List, Optional
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import Response

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/events",
    tags=['Events']
)

limitNumber: int = 10


# LOCK FOR EVERYONE, USE IN FUNCTION PARAM
# current_user: schemas.UserResponseData = Depends(get_current_user)

@router.get('/', response_model=List[schemas.EventResponse])
def all_events(db: Session = Depends(get_db),
              limit: int = limitNumber, skip: int = 0, search: Optional[str] = ""):

    # ONLY AUTHORIZED USER CAN SEE ALL Events
    # myPost = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # USER CAN SEE ALL POSTS
    myEvent = db.query(models.Event).filter(models.Event.title.contains(search)).limit(limit).offset(skip).all()

    return myEvent


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreateRequest, db: Session = Depends(get_db),
                current_user: schemas.UserResponseData = Depends(get_current_user)):

    if current_user.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    print(current_user.id)

    # ORM
    new_event = models.Event(owner_id=current_user.id, **event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get('/{id}', response_model=schemas.EventResponse)
async def get_event(id: int, db: Session = Depends(get_db),
                   current_user: schemas.UserResponseData = Depends(get_current_user)):

    # ORM
    event = db.query(models.Event).filter(models.Event.id == id).first()
    # post = find_post(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your id is not found in our database {id}")

    # ONLY AUTHORIZED USER CAN SEE
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    return event


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, db: Session = Depends(get_db),
                      current_user: schemas.UserResponseData = Depends(get_current_user)):

    event_query = db.query(models.Event).filter(models.Event.id == id)
    event = event_query.first()

    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your event not found in Database")
    # my_posts.pop(index)

    if event.owner_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    event_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.EventResponse)
async def update_event(id: int, updated_event: schemas.EventCreateRequest, db: Session = Depends(get_db),
                      current_user: schemas.UserResponseData = Depends(get_current_user)):

    new_event = db.query(models.Event).filter(models.Event.id == id)
    event = new_event.first()

    # index = find_index(id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found for updating data")

    if event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    new_event.update(updated_event.dict(), synchronize_session=False)
    db.commit()
    db.refresh(event)

    return event
