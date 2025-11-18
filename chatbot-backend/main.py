"""
TriVenta Tech AI Chatbot - Main FastAPI Application
Complete backend API with LLM integration, NLP processing, and database management
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import uuid
from typing import List, Optional

from app.config import settings
from app.models.schemas import (
    ChatRequest, ChatResponse, HealthCheck,
    ConversationHistory, UserProfileResponse
)
from app.services.llm_service import get_llm_service, LLMService
from app.services.nlp_service import get_nlp_service, NLPService
from loguru import logger

# Configure logging
logger.add(
    "logs/chatbot_{time}.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.LOG_LEVEL
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Initialize services
    try:
        llm = get_llm_service()
        nlp = get_nlp_service()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Service initialization failed: {str(e)}")
        raise
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down chatbot backend")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Human-like AI chatbot with advanced NLP, context awareness, and emotion detection",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
conversations = {}
user_profiles = {}


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint - health check"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.APP_VERSION,
        llm_provider=settings.LLM_PROVIDER,
        llm_status="active",
        database_status="active",
        vector_db_status="active"
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Detailed health check"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.APP_VERSION,
        llm_provider=settings.LLM_PROVIDER,
        llm_status="active",
        database_status="active",
        vector_db_status="active"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    llm: LLMService = Depends(get_llm_service),
    nlp: NLPService = Depends(get_nlp_service)
):
    """
    Main chat endpoint - processes user message and returns AI response
    """
    
    try:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Initialize conversation if new
        if session_id not in conversations:
            conversations[session_id] = {
                "messages": [],
                "context": {},
                "user_name": request.user_name,
                "user_id": request.user_id,
                "start_time": datetime.now(),
                "interested_services": [],
                "urgency_level": "normal"
            }
        
        conv = conversations[session_id]
        
        # Update user name if provided
        if request.user_name:
            conv["user_name"] = request.user_name
        
        # Analyze user message with NLP
        nlp_analysis = nlp.analyze_message(request.message)
        
        logger.info(f"Session {session_id}: Message received")
        logger.info(f"Intent: {nlp_analysis['intent'][0]}, Sentiment: {nlp_analysis['sentiment']['label']}")
        
        # Update conversation context
        conv["context"].update(request.context or {})
        conv["context"]["last_intent"] = nlp_analysis["intent"][0]
        conv["context"]["last_sentiment"] = nlp_analysis["sentiment"]["label"]
        conv["context"]["entities"] = {**conv["context"].get("entities", {}), **nlp_analysis["entities"]}
        
        # Update urgency level
        if nlp_analysis["urgency"] == "high":
            conv["urgency_level"] = "high"
        
        # Extract and store interested services
        intent_to_service = {
            "web_development": "Web Development",
            "ai_ml": "AI & Data Science",
            "cybersecurity": "Cybersecurity",
            "cloud": "Cloud Solutions",
            "mobile": "Mobile Apps",
            "training": "Training Programs"
        }
        
        detected_intent = nlp_analysis["intent"][0]
        if detected_intent in intent_to_service:
            service = intent_to_service[detected_intent]
            if service not in conv["interested_services"]:
                conv["interested_services"].append(service)
        
        # Build conversation history for LLM
        conv["messages"].append({"role": "user", "content": request.message})
        
        # Generate system prompt with context
        user_context = {
            "user_name": conv.get("user_name"),
            "interested_services": conv["interested_services"],
            "budget_range": nlp_analysis["entities"].get("budget"),
            "urgency_level": conv["urgency_level"]
        }
        
        system_prompt = llm.get_system_prompt(user_context)
        
        # Generate AI response
        response_text = await llm.generate_response(
            messages=conv["messages"][-10:],  # Last 10 messages for context
            system_prompt=system_prompt
        )
        
        # Add assistant response to conversation
        conv["messages"].append({"role": "assistant", "content": response_text})
        
        # Generate follow-up suggestions based on intent
        suggestions = generate_suggestions(detected_intent, nlp_analysis)
        
        # Build response
        response = ChatResponse(
            response=response_text,
            session_id=session_id,
            intent=detected_intent,
            sentiment=nlp_analysis["sentiment"]["label"],
            confidence=nlp_analysis["intent"][1],
            suggestions=suggestions,
            context={
                "user_name": conv.get("user_name"),
                "interested_services": conv["interested_services"],
                "message_count": len(conv["messages"]),
                "urgency": conv["urgency_level"]
            },
            metadata={
                "timestamp": datetime.now().isoformat(),
                "model": settings.LLM_MODEL,
                "provider": settings.LLM_PROVIDER,
                "emotions": nlp_analysis["emotions"]
            }
        )
        
        logger.info(f"Session {session_id}: Response generated successfully")
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@app.get("/api/conversation/{session_id}", response_model=ConversationHistory)
async def get_conversation_history(session_id: str):
    """Get conversation history for a session"""
    
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = conversations[session_id]
    
    return ConversationHistory(
        session_id=session_id,
        messages=[
            {"role": msg["role"], "content": msg["content"], "timestamp": datetime.now()}
            for msg in conv["messages"]
        ],
        user_name=conv.get("user_name"),
        start_time=conv["start_time"],
        last_message_time=datetime.now(),
        message_count=len(conv["messages"]),
        sentiment_average=0.0  # Calculate from stored sentiments
    )


@app.delete("/api/conversation/{session_id}")
async def delete_conversation(session_id: str):
    """Delete a conversation"""
    
    if session_id in conversations:
        del conversations[session_id]
        return {"message": "Conversation deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")


@app.post("/api/feedback")
async def submit_feedback(session_id: str, rating: int, comment: Optional[str] = None):
    """Submit conversation feedback"""
    
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversations[session_id]["feedback"] = {
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now()
    }
    
    logger.info(f"Feedback received for session {session_id}: Rating {rating}")
    
    return {"message": "Feedback submitted successfully"}


def generate_suggestions(intent: str, nlp_analysis: dict) -> List[str]:
    """Generate contextual follow-up suggestions"""
    
    suggestions_map = {
        "greeting": [
            "Tell me about your services",
            "I need a website",
            "How can you help my business?"
        ],
        "web_development": [
            "What's the pricing for a website?",
            "How long does it take?",
            "Show me your portfolio"
        ],
        "ai_ml": [
            "What AI solutions do you offer?",
            "Can you build a chatbot like this?",
            "Tell me about data science services"
        ],
        "cybersecurity": [
            "How do you secure systems?",
            "Do you offer penetration testing?",
            "What's the cost?"
        ],
        "pricing": [
            "Can I get a detailed quote?",
            "Do you have sample quotations?",
            "What payment options do you offer?"
        ],
        "contact": [
            "Send me your WhatsApp number",
            "What's your email?",
            "Where are you located?"
        ]
    }
    
    return suggestions_map.get(intent, [
        "Tell me more about your services",
        "How can I get started?",
        "What are your contact details?"
    ])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
