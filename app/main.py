from fastapi import FastAPI
from .database import Base, engine
from .models import user, post, comment

app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"message": "FastAPI Reddit Clone"}