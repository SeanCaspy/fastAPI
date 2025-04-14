from fastapi import APIRouter, HTTPException
import bcrypt
from storage import users
from models import LoginRequest, User


router = APIRouter()

@router.post('/register')
def register(req: User):
    if req.username in users:
        raise HTTPException(status_code=400, detail="User name already exist")
    spiecl_chars = {'!','@','#','$','%','^','&','*','(',')'}
    if not any (cha in req.password for cha in spiecl_chars) or len(req.password) <  8:
        raise HTTPException(status_code=400, detail="password must contain one of !@#$%^&*() and length must ne longer than 8")
    if req.username in users:
        raise HTTPException(status_code=400, detail='user already exsit')
    
    hashed = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt())
    users[req.username] = hashed
    return {'message': 'user has been registered'}
    
    
        
