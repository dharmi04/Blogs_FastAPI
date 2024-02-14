from fastapi import APIRouter, Depends, HTTPException, status

import schemas
import models
from typing import List
import database
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router= APIRouter(
    prefix='/user',
    tags=['User']
)
get_db = database.get_db

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', response_model=schemas.ShowUser )
def create_user(request:schemas.User, db:Session = Depends(database.get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get('/{user_id}', response_model=schemas.ShowUser )
def show(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found!!")
    return user

    

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT )
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted successfully!'
