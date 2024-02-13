from fastapi import FastAPI, Depends, HTTPException, Response, status
import schemas
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all( db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def all(id, response:Response, db: Session = Depends(get_db), status_code=200):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found!!")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with id {id} not found!!"}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
     db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
     db.commit()

     return 'deleted!!!!!'



@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(request)
    db.commit()
    return 'updated'
