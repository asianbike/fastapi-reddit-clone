from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..utils.hashing import Hash
from ..utils.token import create_access_token

router = APIRouter()  # ✅ 함수 호출!

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(request: schemas.UserLogin, db: Session = Depends(get_db)):  # ✅ 타입 힌트 + Depends
    user = db.query(models.User).filter(models.User.email == request.email).first()  # ✅ 모델명 정확히
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
