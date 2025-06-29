from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title:str
    content:str


class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    user_id : int

    class config:
        from_attributes = True
