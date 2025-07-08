from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .models import user, post, comment
from .models.user import Base 
from .routers import user as routers_user, auth,comment as comment_router, protected, post as post_router, like as like_router
import os

user.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routers_user.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(like_router.router)
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})
