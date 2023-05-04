from fastapi import APIRouter, Depends, status, Response, HTTPException
import schemas
from database import get_db
import models
from sqlalchemy.orm import Session
from hashing import Hash


router = APIRouter(
                    tags=["User"], prefix="/user"
                )

# @router.post('',status_code=status.HTTP_201_CREATED)
@router.post('',status_code=status.HTTP_201_CREATED,response_model=schemas.UserReturn)
def create_user(request: schemas.UserRequest, response: Response, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.hashing_pd(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    return {"status": 200,
            "detail": "Success",
            "data": new_user}


@router.get('')
def get_all_users(db: Session = Depends(get_db)) -> schemas.UserReturn2:
    all_users = db.query(models.User).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Data Found")
    # l = [schemas.UserReturn(id=user.id,name=user.name,email=user.email,blogs=schemas.UserReturn.from_orm(user)) for user in all_users]
    return_users = [schemas.UserReturn.from_orm(user) for user in all_users]

    # return all_users
    return {"status": 200,
            "detail": "Success",
            "data": return_users}


@router.get('/{id}')
def get_user_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        """
    Get a user by ID.

    Raises:
        HTTPException 404: If the user is not found.
    """
        response.status_code = status.HTTP_404_NOT_FOUND

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Data Found")
        # return {"status": 404,
        #         "detail": "No Data Found",
        #         "data": []}

    # return user
    return {"status": 200,
            "detail": "Success",
            "data": [schemas.UserReturn.from_orm(user)]}
