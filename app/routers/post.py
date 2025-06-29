from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..models import User,Post
from ..schemas import PostResponse,PostCreate
from ..database import get_db # 체크해야함
from ..utils.oauth2 import get_current_user

router = APIRouter()

@router.post("/posts",response_model=PostResponse)
def create_post(
    request:PostCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_user)

):
    new_post=Post(
        title=request.title,
        content=request.content,
        user_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post