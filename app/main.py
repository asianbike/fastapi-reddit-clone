from fastapi import FastAPI,Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import Base, engine,get_db
from .models import user, post, comment
from .models.user import Base 
from .utils.oauth2 import get_current_user
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
    return templates.TemplateResponse("index.html",{
        "request":request,
    })


from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

@app.get("/posts")
def show_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(post.Post).all()
    for p in posts:
        p.comments = db.query(comment.Comment).filter(comment.Comment.post_id == p.id).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@app.post("/posts/new")
def create_post(request: Request, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_post = post.Post(title=title, content=content, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)

@app.post("/posts/{id}/delete")
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post_obj = db.query(post.Post).filter(post.Post.id == id).first()
    if post_obj and post_obj.user_id == current_user.id:
        db.delete(post_obj)
        db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)

@app.post("/comments/new")
def create_comment(request: Request, post_id: int = Form(...), content: str = Form(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_comment = comment.Comment(content=content, post_id=post_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)
