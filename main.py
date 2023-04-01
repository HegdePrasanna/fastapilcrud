from fastapi import FastAPI
from typing import Optional
from schemas import BlogRequest
app = FastAPI()


@app.get("/")
def index():
    return {"status": 200,
            "detail": "Success",
            "data": None}


@app.get("/blogs")
def get_blogs_all(limit=10, sort: Optional[str] = None):
    return {"status": 200,
            "detail": "Success",
            "data": [f"{limit}"]}


@app.get("/blogs/unpublished", description="Get All Unpublished blogs")
def get_blogs_unpublished():
    return {"status": 200,
            "detail": "Success",
            "data": ["List of unpublished blogs"]}


@app.get("/blogs/{id}")
def get_blogs_id(id: int):
    return {"status": 200,
            "detail": "Success",
            "data": [{"id": id}]}


@app.get("/blogs/{id}/comments")
def get_blogs_id_comments(id: int):
    return {"status": 200,
            "detail": "Success",
            "data": [{"id": id,
                     "comments": ["1", "2"]}]}


@app.post("/blogs")
def create_blog(request: BlogRequest):
    return {"status": 200,
            "detail": "Success",
            "data": {"id": request}}
