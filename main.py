from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy  import Engine
import schemas
import models
from database import  get_db, engine
from sqlalchemy.orm import Session
from routers import authencation, blog, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)


app.include_router(authencation.router)
app.include_router(blog.router)
app.include_router(user.router)





