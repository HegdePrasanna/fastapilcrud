from fastapi import FastAPI, Depends, status, Response, HTTPException
# from typing import Optional
from schemas import BlogRequest
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
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


@app.get("/blogs/unpublished", description="Get All Unpublished blogs")
def get_blogs_unpublished():
    return {"status": 200,
            "detail": "Success",
            "data": ["List of unpublished blogs"]}


# @app.get("/blogs/{id}")
# def get_blogs_id(id: int):
#     return {"status": 200,
#             "detail": "Success",
#             "data": [{"id": id}]}


@app.get("/blogs/{id}/comments")
def get_blogs_id_comments(id: int):
    return {"status": 200,
            "detail": "Success",
            "data": [{"id": id,
                     "comments": ["1", "2"]}]}


##########################################################
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"status": 200,
            "detail": "Success",
            "data": blogs}


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(request: BlogRequest, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"status": 200,
            "detail": "Success",
            "data": new_blog}


@app.get("/blogs/{id}")
def get_blogs_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": status.HTTP_404_NOT_FOUND,
        #     "detail": "No Data Found",
        #     "data": []}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Data Found")
    return {"status": 200,
            "detail": "Success",
            "data": [blog]}


@app.delete("/blogs/{id}")
def destroy(id: int, response: Response, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(
        synchronize_session=False)
    db.commit()
    return {"status": 200,
            "detail": "Success",
            "data": []}
