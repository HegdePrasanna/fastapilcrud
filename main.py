from fastapi import FastAPI, Depends, status, Response, HTTPException
# from typing import Optional
from fastapi.encoders import jsonable_encoder
from schemas import BlogRequest,BlogReturn,UserRequest
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from hashing import Hash
from typing import List


app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
def index():
    return {"status": 200,
            "detail": "Success",
            "data": None}


# @app.get("/blogs")
# def get_blogs_all(limit=10, sort: Optional[str] = None):
#     return {"status": 200,
#             "detail": "Success",
#             "data": [f"{limit}"]}


# @app.get("/blogs/unpublished", description="Get All Unpublished blogs")
# def get_blogs_unpublished():
#     return {"status": 200,
#             "detail": "Success",
#             "data": ["List of unpublished blogs"]}


# @app.get("/blogs/{id}")
# def get_blogs_id(id: int):
#     return {"status": 200,
#             "detail": "Success",
#             "data": [{"id": id}]}


# @app.get("/blogs/{id}/comments")
# def get_blogs_id_comments(id: int):
#     return {"status": 200,
#             "detail": "Success",
#             "data": [{"id": id,
#                      "comments": ["1", "2"]}]}


##########################################################
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blogs",response_model=List[BlogReturn])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    # return {"status": 200,
    #         "detail": "Success",
    #         "data": blogs}
    return blogs


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(request: BlogRequest, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"status": 200,
            "detail": "Success",
            "data": new_blog}


# @app.get("/blogs/{id}", response_model=BlogReturn)
@app.get("/blogs/{id}")
def get_blogs_id(id: int, response: Response, db: Session = Depends(get_db)) -> BlogReturn:
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


@app.put("/blogs/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blogs_id(id: int, request:BlogRequest, response: Response, db: Session = Depends(get_db)):
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


@app.delete("/blogs/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, response: Response, db: Session = Depends(get_db)):
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


@app.post('/user',status_code=status.HTTP_201_CREATED)
def create_user(request: UserRequest, db: Session = Depends(get_db)):
    
    new_user = models.User(name=request.name,email=request.email,password=Hash.hashing_pd(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": 200,
            "detail": "Success",
            "data": new_user}