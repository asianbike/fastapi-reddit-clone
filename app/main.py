from fastapi import FastAPI
from .database import Base, engine
from .models import user, post, comment
from .models.user import Base 
from .routers import user as routers_user, auth, protected, post as post_router


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routers_user.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(post_router.router)
@app.get("/")
def root():
    return {"message": "FastAPI Reddit Clone"}