"""
DB session and engine setup.

Style note: Python relies on indentation not braces; we emulate an Allman spirit
by keeping blocks visually open and documented.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = "sqlite:///./tickets.db"

engine = create_engine(
    DB_URL,
    connect_args = {"check_same_thread": False}  # SQLite thread safety for dev
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
