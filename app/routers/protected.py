from fastapi import APIRouter, Depends
from ..utils.oauth2 import get_current_user
from .. import models

router = APIRouter()

@router.get("/me")
def read_current_user(current_user:models.User=Depends(get_current_user)):
    return {
        "email" : current_user.email,
        "username" : current_user.username,
        "id" : current_user.id
    }
