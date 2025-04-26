from fastapi import APIRouter, HTTPException, Depends, Body
import bcrypt
from jose import jwt, JWTError
from models import LoginRequest, RegisterRequest, RefreshTokenRequest, UserDB
from utils.auth_utils import create_access_token, verify_token, create_refresh_token, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

special_chars = {'!','@','#','$','%','^','&','*','(',')'}

@router.post('/register')
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == req.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    if not any(cha in req.password for cha in special_chars) or len(req.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain one of: !@#$%^&*()")

    hashed = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt())
    new_user = UserDB(
        username=req.username,
        hashed_password=hashed.decode('utf-8')
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User has been registered'}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == req.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Username not found. Would you like to register?")
    if not bcrypt.checkpw(req.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Wrong password. Try again.")
    
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/protected")
def protected_route(user_id: int = Depends(verify_token)):
    return {"message": f"Hello user with ID {user_id}, you have accessed a protected route!"}

@router.post("/refresh")
def refresh_access_token(req: RefreshTokenRequest):
    try:
        payload = jwt.decode(req.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token = create_access_token(data={"user_id": user_id})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Refresh Token")
