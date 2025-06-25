from fastapi import FastAPI
from .database import Base, engine
from .routers import user
from .models import user, post, comment
from .routers import user, auth, protected

user.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(protected.router)
@app.get("/")
def root():
    return {"message": "FastAPI Reddit Clone"}