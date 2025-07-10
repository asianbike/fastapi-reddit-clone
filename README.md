# 🧪 FastAPI Reddit Clone

A full-stack backend clone of Reddit built with FastAPI, SQLAlchemy, PostgreSQL, and JWT-based authentication.

---

## 📦 Features

- 📝 **User Registration**: Register with email, username, and password
- 🔐 **JWT Authentication**: Login and receive a secure access token
- 🧾 **Protected Routes**: Use token to access authenticated endpoints
- 📢 **Post Creation**: Authenticated users can create posts
- ⚙️ **ORM Models**: SQLAlchemy used to model `User`, `Post`, and `Comment`
- 🚀 **Auto-Reload Dev Server**: Uvicorn with `--reload`

---

## 🧰 Tech Stack

| Category | Tech |
|----------|------|
| Backend Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Authentication | OAuth2PasswordBearer, JWT (with python-jose) |
| Password Security | Passlib (bcrypt) |
| Dev Tools | Docker (soon), VS Code, Curl, Swagger UI |
| Others | Pydantic, Uvicorn |

---

## 🔧 How to Run

1. Clone the repo  
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-reddit-clone.git
cd fastapi-reddit-clone

    Set up virtual environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

    Start dev server

uvicorn app.main:app --reload

    Open browser
    → http://127.0.0.1:8000/docs

📬 Current Status

✅ User signup/login API completed
✅ JWT token-based protected routes implemented
✅ Post creation feature working with DB
🛠️ Comment system to be implemented next
📌 Docker deployment + CI/CD planned
🔑 Example Credentials for Testing

{
  "email": "user@example.com",
  "password": "string"
}

Use this to test /login, get token, and use /me, /posts.
🧠 Learning Purpose

This project is part of my preparation for backend SWE internships at Big Tech companies in North America.
Built from scratch with guidance to deeply understand how real authentication, ORM, REST API, and token-based systems work.
📌 Author
