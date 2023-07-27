from fastapi import Response, status as HTTPStatus, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts",
                   tags=["posts"])

@router.get("/", response_model=List[schemas.PostResponse]) # ret val posts is a list, so we need to listify schema
def get_posts(db:Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code = HTTPStatus.HTTP_201_CREATED, response_model=schemas.PostResponse) # best practice is to use /posts
def create_posts(post : schemas.CreatePost, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # using pydantic to build schema for input request   
    # NEVER DO an f String, since if we have sql as the input data, it will do sql injection attack. %s will sanitize the input
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit() 
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse) # the id field is a path parameter, represents ID of specific post
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",str(id))
    # data = cursor.fetchone()
    # if not data:
    #     raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND,
    #                         detail = f"Post with id:{id} not found")
    # return {"post_detail":data}
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()
    if not post:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND,
                            detail = f"Post with id:{id} not found")
    return post

@router.delete("/{id}", status_code=HTTPStatus.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # data = cursor.fetchone()
    # conn.commit()
    # if data == None:
    #     raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist")
    
    # return Response(status_code=HTTPStatus.HTTP_204_NO_CONTENT)
    post = db.query(models.Post).filter(models.Post.id == str(id))
    if post.first() == None:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTPStatus.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published, str(id)))
    # data = cursor.fetchone()
    # conn.commit()
    # if data == None:
    #     raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist")    
    # return {"data": data} 
    posts = db.query(models.Post).filter(models.Post.id == str(id))
    post = posts.first()
    if post == None:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist")
    posts.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return posts.first()