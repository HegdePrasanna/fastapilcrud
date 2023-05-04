from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
import schemas
from hashing import Hash
from database import get_db

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(request:schemas.LoginRequest,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username or User.name == request.username).first()
    if not user:
        raise HTTPException(detail="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify_pw(user.password,request.password):
        raise HTTPException(detail="Password Does Not Match",status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return user