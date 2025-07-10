from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    content : str
    post_id : int

class CommentResponse(BaseModel):
    id : int
    content : str
    post_id : int

    class Config:
        from_attributes =True