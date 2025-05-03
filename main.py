from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, posts
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

app = FastAPI()

# @app.get("/", response_class=FileResponse)
# def read_root():
#     return "frontend/index.html"

users = []

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)

Base.metadata.create_all(bind=engine)


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")