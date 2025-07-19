from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserCreate, UserLogin, UserResponse, PostCreate, PostResponse, CommentCreate, CommentResponse
from auth import hash_password, verify_password, create_access_token
from database import get_db
from crud import get_posts, create_post, update_post, delete_post, get_comments, create_comment, create_user, get_user_by_email
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from models import User
from schemas import UserResponse
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

router = APIRouter()

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = await create_user(db, user)
    return db_user

@auth_router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

# Posts router
posts_router = APIRouter(prefix="/posts", tags=["posts"])

@posts_router.get("/", response_model=List[PostResponse])
async def list_posts(db: AsyncSession = Depends(get_db)):
    posts = await get_posts(db)
    return posts

@posts_router.post("/", response_model=PostResponse)
async def create_post_endpoint(post: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = await create_post(db, post, str(current_user.id))
    return db_post

@posts_router.put("/{id}", response_model=PostResponse)
async def update_post_endpoint(id: str, post: PostCreate, db: AsyncSession = Depends(get_db)):
    db_post = await update_post(db, id, post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@posts_router.delete("/{id}")
async def delete_post_endpoint(id: str, db: AsyncSession = Depends(get_db)):
    success = await delete_post(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post {id} deleted"}

# Comments router (still placeholder)
comments_router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@comments_router.get("/", response_model=List[CommentResponse])
async def list_comments(post_id: str, db: AsyncSession = Depends(get_db)):
    comments = await get_comments(db, post_id)
    return comments

@comments_router.post("/", response_model=CommentResponse)
async def add_comment(post_id: str, comment: CommentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = await create_comment(db, post_id, comment, str(current_user.id))
    return db_comment

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Placeholder for avatar upload endpoint
@user_router.post("/me/avatar")
async def upload_avatar():
    return {"message": "Avatar upload not implemented yet"}

# Attach all routers to the main router
router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(comments_router)
router.include_router(user_router) 