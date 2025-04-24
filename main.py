from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, posts
import bcrypt
from database import Base, engine
import models

app = FastAPI()

users = []



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אפשר לאפשר לכתובות ספציפיות במקום כוכבית בעתיד
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)

Base.metadata.create_all(bind=engine)

