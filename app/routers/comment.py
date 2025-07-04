from fastapi import APIRouter, Depends, HTTPException,status,Path
from sqlalchemy.orm import Session
from ..models import User,Comment
from ..schemas import CommentCreate,CommentResponse
from ..database import get_db 
from ..utils.oauth2 import get_current_user

router = APIRouter()

@router.post("/comments",response_model=CommentResponse)
def create_comment(
    request: CommentCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    new_comment=Comment(
        content=request.content,
        user_id=current_user.id,
        post_id=request.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/comments/{post_id}",response_model=list[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.get("/comments", response_model=list[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()
