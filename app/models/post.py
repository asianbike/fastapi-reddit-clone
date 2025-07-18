from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id=Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=True)
    content=Column(Text, nullable=True)
