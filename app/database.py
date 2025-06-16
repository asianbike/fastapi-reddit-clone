from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from .database import Base

engine = create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
