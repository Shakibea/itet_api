from typing import List, Optional
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import Response

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

limitNumber: int = 10


@router.get('/', response_model=List[schemas.PostResponse])
def all_posts(db: Session = Depends(get_db), current_user: schemas.UserResponseData = Depends(get_current_user),
              limit: int = limitNumber, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts;")
    # myPost = cursor.fetchall()

    # ONLY AUTHORIZED USER CAN SEE ALL POSTS
    # myPost = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # USER CAN SEE ALL POSTS
    myPost = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return myPost


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreateRequest, db: Session = Depends(get_db),
                current_user: schemas.UserResponseData = Depends(get_current_user)):
    # Raw SQL
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published,))
    # new_post = cursor.fetchone()
    # conn.commit()

    if current_user.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    print(current_user.id)

    # ORM
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # print(f"your post: {post.dict()}")
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000)
    # my_posts.append(post_dict)
    return new_post


@router.get('/{id}', response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: schemas.UserResponseData = Depends(get_current_user)):
    # Raw Sql
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your id is not found in our database {id}")

    # ONLY AUTHORIZED USER CAN SEE
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: schemas.UserResponseData = Depends(get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # index = find_index(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your post not found in Database")
    # my_posts.pop(index)

    if post.owner_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreateRequest, db: Session = Depends(get_db),
                      current_user: schemas.UserResponseData = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, id,))
    # fetchUpdatePost = cursor.fetchone()
    # conn.commit()

    new_post = db.query(models.Post).filter(models.Post.id == id)
    post = new_post.first()

    # index = find_index(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found for updating data")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the action!")

    new_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post
