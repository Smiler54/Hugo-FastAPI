from fastapi import FastAPI
from routers import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hugo-FastAPI News Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:1313"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hugo-FastAPI News Platform API!"}

# Placeholder for user, post, and comment routers
# from .routers import users, posts, comments
# app.include_router(users.router)
# app.include_router(posts.router)
# app.include_router(comments.router) 