from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Comment(Base):
    __tablename__ = "comments"

    id=Column(Integer,primary_key=True,index=True)
    content=Column(Text,nullable=False)
    post_id=Column(Integer, ForeignKey("posts.id"))

   
   