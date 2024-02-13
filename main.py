from fastapi import FastAPI, Depends, HTTPException, Response, status
import schemas
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'] )
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog' , tags=['blogs'])
def all( db: Session = Depends(get_db), response_model = schemas.ShowBlog):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}' , tags=['blogs'])
def all(id, response:Response, db: Session = Depends(get_db), status_code=200,  response_model = schemas.ShowBlog):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found!!")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with id {id} not found!!"}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT , tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
     db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
     db.commit()

     return 'deleted!!!!!'



@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED , tags=['blogs'])
def update(id, request:schemas.Blog, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(request)
    db.commit()
    return 'updated'





pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', response_model=schemas.ShowUser , tags=['Users'])
def create_user(request:schemas.User, db:Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@app.get('/user/{user_id}', response_model=schemas.ShowUser , tags=['Users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found!!")
    return user

    

@app.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT , tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted successfully!'

