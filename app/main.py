from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from .database import Base, engine,get_db
from .models import user, post, comment
from .models.user import Base,User
from .utils.oauth2 import get_current_user
from .routers import user as routers_user, auth,comment as comment_router, protected, post as post_router, like as like_router
import os
from fastapi import Form, Response, Cookie
from jose import jwt
from .utils.hashing import Hash
import datetime

user.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routers_user.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(comment_router.router)
app.include_router(like_router.router)
app.include_router(post_router.router)

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

# 글 작성
@app.post("/posts/new")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    new_post = post.Post(title=title, content=content, user_id=1)  # 테스트용 user_id=1 고정
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)


# 글 삭제
@app.post("/posts/{id}/delete")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_obj = db.query(post.Post).filter(post.Post.id == id).first()
    if post_obj:
        db.delete(post_obj)
        db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)


# 댓글 작성
@app.post("/comments/new")
def create_comment(
    request: Request,
    post_id: int = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    new_comment = comment.Comment(content=content, post_id=post_id, user_id=1)  # 테스트용 user_id=1
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)


# 댓글 삭제
@app.post("/comments/{id}/delete")
def delete_comment(id: int, db: Session = Depends(get_db)):
    comment_obj = db.query(comment.Comment).filter(comment.Comment.id == id).first()
    if comment_obj:
        db.delete(comment_obj)
        db.commit()
    return RedirectResponse(url="/posts", status_code=HTTP_303_SEE_OTHER)

@app.get("/view/posts/{post_id}")
def view_post_detail(post_id: int, request: Request, db: Session = Depends(get_db)):
    post_obj = db.query(post.Post).filter(post.Post.id == post_id).first()
    if not post_obj:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_obj.comments = db.query(comment.Comment).filter(comment.Comment.post_id == post_id).all()

    return templates.TemplateResponse("post_detail.html", {
        "request": request,
        "post": post_obj
    })

SECRET_KEY = "your_secret"
ALGORITHM = "HS256"

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(
    request:Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    userr = db.query(User).filter(User.email == email).first()
    if not userr or not Hash.verify(password, userr.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

    token = jwt.encode({"sub": userr.email}, SECRET_KEY, algorithm=ALGORITHM)
    res = RedirectResponse(url="/posts", status_code=303)
    res.set_cookie(key="access_token", value=token, httponly=True)
    return RedirectResponse(url="/posts", status_code=303)

@app.get("/logout")
def logout_user():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

@app.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup_user(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # routers/user.py와 중복되지 않게 form 기반 처리
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "email already exists"
        })

    new_user = User(
        email=email,
        username=username,
        hashed_password=Hash.bcrypt(password)
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)