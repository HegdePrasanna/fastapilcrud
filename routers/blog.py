from fastapi import APIRouter, Depends, status, Response, HTTPException
import schemas
from typing import List
from database import get_db
import models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from repository import blog
import schemas
from OAuth2 import get_current_user

router = APIRouter(
                    tags=["Blogs"], prefix="/blog"
                )


@router.get("",response_model=List[schemas.BlogReturn])
def get_all_blogs(db: Session = Depends(get_db),current_user:schemas.UserReturn1=Depends(get_current_user)):
    # blogs = db.query(models.Blog).all()
    # # return {"status": 200,
    # #         "detail": "Success",
    # #         "data": blogs}
    # return blogs
    return blog.get_all(db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogRequest, db: Session = Depends(get_db),
                current_user:schemas.UserReturn1=Depends(get_current_user)) -> schemas.BlogReturnMain:
    # new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    return blog.create(db,request)
    # return {"status": 201,
    #         "detail": "Success",
    #         "data": new_blog}

#  @router.get("/blogs/{id}", response_model=BlogReturn)
@router.get("/{id}")
def get_blogs_id(id: int, response: Response, db: Session = Depends(get_db),
                 current_user:schemas.UserReturn1=Depends(get_current_user)) -> schemas.BlogReturn:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": status.HTTP_404_NOT_FOUND,
        #     "detail": "No Data Found",
        #     "data": []}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Data Found")
    # return {"status": 200,
    #         "detail": "Success",
    #         "data": [blog]}
    return blog


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blogs_id(id: int, request:schemas.BlogRequest, response: Response, db: Session = Depends(get_db),
                    current_user:schemas.UserReturn1=Depends(get_current_user)):
    request = jsonable_encoder(request)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": status.HTTP_404_NOT_FOUND,
                "detail": "Data Not Found",
                "data": []}
    blog.update(request)
    db.commit()
    return {"status": 200,
            "detail": "Success",
            "data": [blog.first()]}


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Blogs"])
def destroy(id: int, response: Response, db: Session = Depends(get_db),
            current_user:schemas.UserReturn1=Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": status.HTTP_404_NOT_FOUND,
                "detail": "Data Not Found",
                "data": []}
    blog.delete(synchronize_session=False)
    db.commit()
    return {"status": 204,
            "detail": "Success",
            "data": []}