import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments') 