# hiremebackend/database_module.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use PostgreSQL or fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./test.db"

# Create engine with PostgreSQL SSL support if needed
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
