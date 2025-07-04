from pydantic import BaseModel

class LikeCreate(BaseModel):
    post_id: int

class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True