from sqlalchemy.orm import Session
import models
import schemas
def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(db:Session,request:schemas.BlogRequest):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"status": 201,
            "detail": "Success",
            "data": new_blog}