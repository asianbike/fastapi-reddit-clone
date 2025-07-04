from fastapi import APIRouter, Depends, HTTPException,status,Path
from sqlalchemy.orm import Session
from ..models import User,Comment,Like
from ..schemas import LikeResponse,LikeCreate
from ..database import get_db 
from ..utils.oauth2 import get_current_user

router=APIRouter()

@router.post("/likes", response_model=LikeResponse)
def like_post(request: LikeCreate, db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    like =db.query(Like).filter(Like.user_id == current_user.id,Like.post_id==request.post_id).first()
    if like:
        raise HTTPException(status_code=400, detail="Already Liked")
    new_like = Like(post_id=request.post_id,user_id=current_user.id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@router.get("/likes/{post_id}", response_model=int)
def count_likes(post_id: int, db: Session = Depends(get_db)):
    return db.query(Like).filter(Like.post_id == post_id).count()

@router.get("/likes")
def get_all_likes(db: Session = Depends(get_db)):
    return db.query(Like).all()