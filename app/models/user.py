from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password= Column(String, nullable=True)
    username=Column(String, unique=True, nullable=True)

    

    
