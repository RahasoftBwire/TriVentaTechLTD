"""
TriVenta Tech AI Chatbot - Database Models
SQLAlchemy models for conversation storage
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Conversation(Base):
    """Store conversation sessions"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(100), index=True, nullable=True)
    user_name = Column(String(100), nullable=True)
    user_email = Column(String(255), nullable=True)
    user_phone = Column(String(50), nullable=True)
    
    # Conversation metadata
    start_time = Column(DateTime, default=func.now())
    last_message_time = Column(DateTime, default=func.now(), onupdate=func.now())
    message_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # User preferences and context
    user_preferences = Column(JSON, default={})
    conversation_context = Column(JSON, default={})
    
    # Business context
    interested_services = Column(JSON, default=[])
    budget_range = Column(String(50), nullable=True)
    timeline = Column(String(50), nullable=True)
    urgency_level = Column(String(20), default="normal")
    
    # Analytics
    sentiment_average = Column(Float, default=0.0)
    satisfaction_score = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Message(Base):
    """Store individual messages"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # NLP Analysis
    intent = Column(String(100), nullable=True)
    sentiment = Column(String(20), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    emotions = Column(JSON, default=[])
    entities = Column(JSON, default={})
    
    # Response metadata
    response_time = Column(Float, nullable=True)  # seconds
    token_count = Column(Integer, nullable=True)
    model_used = Column(String(50), nullable=True)
    
    # Quality & Safety
    toxicity_score = Column(Float, default=0.0)
    flagged = Column(Boolean, default=False)
    
    timestamp = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())


class UserProfile(Base):
    """Store long-term user profiles"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    
    # User info
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(200), nullable=True)
    
    # Preferences & History
    preferred_language = Column(String(10), default="en")
    preferred_contact_method = Column(String(20), nullable=True)
    communication_style = Column(String(50), default="friendly")
    
    # Interaction history
    total_conversations = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    average_sentiment = Column(Float, default=0.0)
    last_interaction = Column(DateTime, nullable=True)
    
    # Business context
    services_discussed = Column(JSON, default=[])
    projects_quoted = Column(JSON, default=[])
    interests = Column(JSON, default=[])
    
    # Learning & Memory
    user_facts = Column(JSON, default={})  # Long-term memory
    conversation_summaries = Column(JSON, default=[])
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class KnowledgeBase(Base):
    """Store company knowledge base"""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), index=True)
    tags = Column(JSON, default=[])
    
    # Embedding
    embedding_id = Column(String(100), unique=True, nullable=True)
    
    # Metadata
    source = Column(String(255), nullable=True)
    url = Column(String(500), nullable=True)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Usage stats
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
