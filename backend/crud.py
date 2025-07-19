from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from models import Post, Comment, User
from schemas import PostCreate, CommentCreate, UserCreate
import uuid
from datetime import datetime
from auth import hash_password

async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()

async def create_post(db: AsyncSession, post: PostCreate, user_id: str):
    db_post = Post(
        id=uuid.uuid4(),
        user_id=user_id,
        title=post.title,
        text=post.text,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def update_post(db: AsyncSession, post_id: str, post: PostCreate):
    stmt = (
        sqlalchemy_update(Post)
        .where(Post.id == post_id)
        .values(title=post.title, text=post.text, updated_at=datetime.utcnow())
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()

async def delete_post(db: AsyncSession, post_id: str):
    stmt = sqlalchemy_delete(Post).where(Post.id == post_id)
    await db.execute(stmt)
    await db.commit()
    return True

# --- Comments CRUD ---
async def get_comments(db: AsyncSession, post_id: str):
    result = await db.execute(select(Comment).where(Comment.post_id == post_id))
    return result.scalars().all()

async def create_comment(db: AsyncSession, post_id: str, comment: CommentCreate, user_id: str):
    db_comment = Comment(
        id=uuid.uuid4(),
        post_id=post_id,
        user_id=user_id,
        title=comment.title,
        text=comment.text,
        created_at=datetime.utcnow()
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        id=uuid.uuid4(),
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        avatar=user.avatar
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() 