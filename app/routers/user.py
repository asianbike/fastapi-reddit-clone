from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from ..database import SessionLocal
from ..utils.hashing import Hash

router = APIRouter()

# ▶ 의존성 주입: 요청마다 DB 세션을 자동으로 주입받는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ▶ 회원가입 API
@router.post("/signup", response_model=UserResponse)
def create_user(request:UserCreate, db:Session=Depends(get_db)):
    #1. email dupe check
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    
    #2. hashing pw and save db
    new_user = User(
        email=request.email,
        username=request.username,
        hashed_password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
