from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import PostDB, UserDB, PostCreate
from database import get_db
from utils.auth_utils import verify_token

router = APIRouter()

@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db), username: str = Depends(verify_token)):
    user = db.query(UserDB). filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    new_post = PostDB(title=post.title, content=post.content, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "post created", "post_id": new_post.id}

@router.get("/posts")
def get_all_post(db: Session=Depends(get_db)):
    posts = db.query(PostDB).all()
    return posts

@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post