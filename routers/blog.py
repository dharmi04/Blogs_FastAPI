from fastapi import APIRouter, Depends, HTTPException, Response, status
import schemas
import models, oauth2
from typing import List
import database
from sqlalchemy.orm import Session
from repository import blog


router= APIRouter(
    prefix="/blog",
    tags=['Blogs']
)
get_db = database.get_db

@router.get('/')
def all( db: Session = Depends(database.get_db), get_current_user: schemas.User= Depends(oauth2.get_current_user), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,  )
def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
   return blog.create(request, db)



@router.get('/{id}' )
def all(id, response:Response, db: Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found!!")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with id {id} not found!!"}
    return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT )
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
     return blog.destroy(id,db)



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED )
def update(id, request:schemas.Blog, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)





