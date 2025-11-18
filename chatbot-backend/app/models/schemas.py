"""
TriVenta Tech AI Chatbot - Pydantic Schemas
Request/Response models for API endpoints
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat API request"""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="User ID for long-term memory")
    user_name: Optional[str] = Field(None, description="User's name")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context")


class ChatResponse(BaseModel):
    """Chat API response"""
    response: str = Field(..., description="Chatbot response")
    session_id: str = Field(..., description="Session ID")
    intent: Optional[str] = Field(None, description="Detected user intent")
    sentiment: Optional[str] = Field(None, description="Detected sentiment")
    confidence: Optional[float] = Field(None, description="Response confidence")
    suggestions: Optional[List[str]] = Field(default=[], description="Suggested follow-up questions")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Updated context")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Response metadata")


class ConversationHistory(BaseModel):
    """Conversation history response"""
    session_id: str
    messages: List[ChatMessage]
    user_name: Optional[str] = None
    start_time: datetime
    last_message_time: datetime
    message_count: int
    sentiment_average: float


class UserProfileResponse(BaseModel):
    """User profile data"""
    user_id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    total_conversations: int
    total_messages: int
    average_sentiment: float
    last_interaction: Optional[datetime] = None
    interests: List[str] = []


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime
    version: str
    llm_provider: str
    llm_status: str
    database_status: str
    vector_db_status: str
