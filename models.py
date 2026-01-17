"""Database models for LinkedIn post generator."""

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class LinkedInPost(Base):
    """Model for storing LinkedIn posts."""

    __tablename__ = "linkedin_posts"

    id = Column(Integer, primary_key=True, index=True)
    post_type = Column(String(50), index=True)  # story, how-to, list, question, insight, etc.
    content = Column(Text, nullable=False)
    engagement_score = Column(Integer, default=0)  # Proxy for virality (likes, comments, shares)
    author = Column(String(100))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LinkedInPost(id={self.id}, type={self.post_type}, engagement={self.engagement_score})>"


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./linkedin_posts.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
