from sqlalchemy.ext.declarative import declarative_base
# Model class base
Base=declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from .database import Base
# 1 PostgreSQL connect engine
engine = create_engine(DATABASE_URL)
# 2 DB session for every call
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
