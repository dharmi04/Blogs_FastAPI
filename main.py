from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy  import Engine
import schemas
import models
from database import  get_db, engine
from sqlalchemy.orm import Session
from routers import authencation, blog, user

app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(authencation.router)
app.include_router(blog.router)
app.include_router(user.router)





