from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import PostDB, UserDB
from database import get_db
from utils.auth_utils import verify_token
from typing import List
from schemas import PostCreate, PostOut

router = APIRouter()

@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    user = db.query(UserDB). filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    new_post = PostDB(title=post.title, content=post.content, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "post created", "post_id": new_post.id}

@router.get("/posts", response_model=List[PostOut])
def get_all_post(db: Session=Depends(get_db)):
    posts = db.query(PostDB).all()
    return posts

@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

@router.put("/posts/{post_id}")
def update_post(post_id: int, post_update: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = db.query(UserDB).filter(UserDB.id == post.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can update post")
    
    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)

    return {"message": "Post updated", "post": {"id": post.id, "title": post.title, "content": post.content}}

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session=Depends(get_db), user_id: int = Depends(verify_token)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.owner_id != user_id:
        raise HTTPException(status_code=405, detail="only owner can delete post")
    db.delete(post)
    db.commit()
    return{"message":"post deleted"}
