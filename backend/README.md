# Backend (FastAPI)

This directory contains the FastAPI backend for the news platform.

## Features
- RESTful API for users, posts, and comments
- User authentication (JWT/session, password hashing)
- PostgreSQL database (SQLAlchemy models)
- Pydantic schemas for API validation

## Structure
- `main.py` — FastAPI entrypoint
- `models.py` — SQLAlchemy models
- `schemas.py` — Pydantic schemas
- `database.py` — Database connection
- `crud.py` — CRUD operations
- `auth.py` — Authentication logic
- `routers.py` — API routers
- `config.py` — Configuration

## Setup (Outline)
- Configure environment variables (see `config.py`)
- Run database migrations
- Start FastAPI server

> See project root README.md for full instructions. 