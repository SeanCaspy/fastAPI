from fastapi import APIRouter, HTTPException, Depends
import bcrypt
from storage import users
from models import LoginRequest, RegisterRequest
from utils.auth_utils import create_access_token, verify_token


router = APIRouter()

special_chars = {'!','@','#','$','%','^','&','*','(',')'}

@router.post('/register')
def register(req: RegisterRequest):
    if req.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    if not any (cha in req.password for cha in special_chars) or len(req.password) <  8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain one of: !@#$%^&*()")

    
    hashed = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt())
    users[req.username] = hashed
    return {'message': 'user has been registered'}

@router.post("/login")
def login(req: LoginRequest):
    if req.username not in users:
        raise HTTPException(status_code=400, detail="Username not found. Would you like to register?")
    if  not bcrypt.checkpw(req.password.encode('utf-8'), users[req.username]):
        raise HTTPException(status_code=401, detail="Wrong password. Try again.")
    access_token  = create_access_token(data={"sub":req.username})
    return {"access_token":access_token, "token_type":"bearer"}

@router.get("/protected")
def protected_route(username: str = Depends(verify_token)):
        return {"message": f"Hello {username}, you have accessed a protected route!"}



    
    
        
