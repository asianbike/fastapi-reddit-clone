from fastapi import APIRouter, Depends, HTTPException,status,Path
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



@router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int = Path(..., title="The ID of the post to retrieve"), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    return post

@router.put("/posts/{id}", response_model=PostResponse)
def update_post(
    id : int,
    request : PostCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    if post.user_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not authorized to this post")
    
    post.title = request.title
    post.content=request.content
    db.commit()
    db.refresh(post)
    return post
@router.delete("/posts/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message": f"Post with ID {id} has been deleted"}
