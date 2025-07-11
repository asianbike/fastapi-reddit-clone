# 🧠 Mini Reddit Clone (FastAPI + PostgreSQL)

[👉 Live Demo](https://redditclone-sf2l.onrender.com/)

---

## 📌 Overview

This is a **mini Reddit clone** built with **FastAPI** and **PostgreSQL**, featuring basic post and comment functionality.  
The project was created for backend practice, full-stack integration, and deployment experience.

> Live Link: https://redditclone-sf2l.onrender.com/

---

## 🛠 Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL (Hosted on Render)
- **Templating**: Jinja2
- **Server**: Uvicorn
- **Deployment**: [Render](https://render.com/)

---

## 🚀 Features

- Create and view posts
- Comment on posts
- Post detail pages
- Basic HTML interface with Jinja2 templates


## ⚙️ How to Run Locally

```bash
git clone https://github.com/yourusername/fastapi-reddit-clone.git
cd fastapi-reddit-clone

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Set environment variables manually or via .env
# export DATABASE_URL="your_postgresql_url"
# export SECRET_KEY="your_secret_key"

uvicorn app.main:app --reload