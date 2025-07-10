from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id=Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=True)
    content=Column(Text, nullable=True)
    user_id=Column(Integer, ForeignKey("users.id"),nullable=True)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", backref="posts",cascade="all, delete")