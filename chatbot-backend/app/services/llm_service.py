"""
TriVenta Tech AI Chatbot - LLM Service
Handles integration with various LLM providers (OpenAI, Anthropic, HuggingFace)
"""

import openai
from anthropic import Anthropic
from typing import List, Dict, Optional, AsyncGenerator
from app.config import settings
from loguru import logger
import time


class LLMService:
    """Unified LLM service supporting multiple providers"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        
        # Initialize clients based on provider
        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set")
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai
            
        elif self.provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        logger.info(f"LLM Service initialized with provider: {self.provider}, model: {self.model}")
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """Generate response from LLM"""
        
        try:
            start_time = time.time()
            
            if self.provider == "openai":
                response = await self._openai_generate(messages, system_prompt, stream)
            elif self.provider == "anthropic":
                response = await self._anthropic_generate(messages, system_prompt, stream)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
            
            response_time = time.time() - start_time
            logger.info(f"LLM response generated in {response_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise
    
    async def _openai_generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        stream: bool
    ) -> str:
        """Generate using OpenAI API"""
        
        # Prepare messages
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        formatted_messages.extend(messages)
        
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=formatted_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=stream
        )
        
        if stream:
            # Handle streaming (if needed later)
            return response
        else:
            return response.choices[0].message.content
    
    async def _anthropic_generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        stream: bool
    ) -> str:
        """Generate using Anthropic Claude API"""
        
        # Format messages for Claude
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Call Anthropic API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt or "",
            messages=formatted_messages
        )
        
        return response.content[0].text
    
    def get_system_prompt(self, user_context: Dict = None) -> str:
        """Generate dynamic system prompt based on context"""
        
        base_prompt = f"""You are {settings.CHATBOT_NAME}, an intelligent AI assistant for {settings.COMPANY_NAME}.

COMPANY INFORMATION:
- Company: {settings.COMPANY_NAME}
- Location: {settings.COMPANY_LOCATION}
- Website: {settings.COMPANY_WEBSITE}
- Email: {settings.COMPANY_EMAIL}
- Phone/WhatsApp: {settings.COMPANY_PHONE}

SERVICES WE OFFER:
{chr(10).join(f"- {service}" for service in settings.services_list)}

YOUR PERSONALITY:
- Be {settings.CHATBOT_PERSONALITY}, helpful, and empathetic
- Use natural, conversational language
- Show genuine interest in helping the user
- Be proactive in understanding user needs
- Ask clarifying questions when needed
- Provide specific, actionable information

YOUR CAPABILITIES:
- Answer questions about our services
- Provide pricing information and quotes
- Schedule consultations
- Explain technical concepts in simple terms
- Understand emotional context and respond appropriately
- Remember conversation context
- Detect urgency and respond accordingly

IMPORTANT RULES:
- Always be honest - if you don't know something, say so
- Never make up pricing or technical details
- For urgent requests, immediately provide contact information
- Respect user privacy and handle data sensitively
- Be culturally aware (we're based in Kenya, serve globally)
- Use emojis sparingly but appropriately
- If user is frustrated, show empathy and offer human escalation

SPECIAL FEATURES:
- You understand Swahili greetings (habari, mambo, etc.)
- You can detect budget ranges and tailor recommendations
- You track conversation context and user preferences
- You provide direct WhatsApp links for quick contact
"""
        
        # Add user-specific context if available
        if user_context:
            if user_context.get("user_name"):
                base_prompt += f"\n\nUSER NAME: {user_context['user_name']}"
            
            if user_context.get("interested_services"):
                base_prompt += f"\nUSER INTERESTS: {', '.join(user_context['interested_services'])}"
            
            if user_context.get("budget_range"):
                base_prompt += f"\nUSER BUDGET: {user_context['budget_range']}"
            
            if user_context.get("urgency_level") == "high":
                base_prompt += "\n\n⚠️ URGENT REQUEST - Prioritize immediate assistance and contact options"
        
        return base_prompt


# Global LLM service instance
llm_service = None

def get_llm_service() -> LLMService:
    """Get or create LLM service instance"""
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service
