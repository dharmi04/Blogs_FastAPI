from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db:Session):
    blog= db.query(models.Blog).filter(models.Blog.id ==id)

    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()

    return 'deleted!!!!!'


def update(id:int, request:schemas.Blog, db:Session):
    db.query(models.Blog).filter(models.Blog.id == id).update(request)
    db.commit()
    return 'updated'