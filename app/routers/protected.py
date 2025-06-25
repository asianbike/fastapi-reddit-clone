from fastapi import APIRouter, Depends
from ..utils.oauth2 import get_current_user
from ..models.user import User

router = APIRouter()

@router.get("/me")
def read_current_user(current_user:User=Depends(get_current_user)):
    return {
        "id" : current_user.id,
        "email" : current_user.email,
        "username" : current_user.username,
    }
