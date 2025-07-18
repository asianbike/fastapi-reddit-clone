from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class Like(Base):
    __tablename__ = "likes"

    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    post_id=Column(Integer, ForeignKey("posts.id"))
    