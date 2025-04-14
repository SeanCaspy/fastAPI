from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

users = []

class User(BaseModel):
    name: str  = Field( min_length=1)
    age: int = Field(gt=12, lt=100)

@app.get('/')
def read_root():
    return {'message': 'welcome to my first api'}

@app.post('/create_user')
def create(user: User):
    for u in users:
        if user.name == u.name and user.age == u.age:
            return {'message':"the user is already in the system"}
    users.append(user)
    return {"message":f"hello {user.name}, you're {user.age} years old"}

@app.get('/hello')
def say_hello(name: str = 'Sean'):
    return {'message' : f"hello {name}"}

@app.get('/users')
def show_users():
    return {'message': users}



