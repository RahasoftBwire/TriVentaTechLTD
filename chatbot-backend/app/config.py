"""
Bwire Global Tech AI Chatbot - Configuration Manager
Loads environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000
    
    # Vector Database
    VECTOR_DB: str = "chromadb"
    VECTOR_DB_PATH: str = "./data/vector_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/chatbot.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://www.triventatech.com"
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Application
    APP_NAME: str = "Bwire Global Tech AI Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Chatbot
    CHATBOT_NAME: str = "TriVenta AI"
    CHATBOT_PERSONALITY: str = "friendly"
    CHATBOT_LANGUAGE: str = "en"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 50
    RATE_LIMIT_PERIOD: int = 60
    
    # Safety
    ENABLE_CONTENT_FILTER: bool = True
    ENABLE_TOXICITY_CHECK: bool = True
    MAX_CONVERSATION_LENGTH: int = 50
    
    # Business Context
    COMPANY_NAME: str = "Bwire Global Tech"
    COMPANY_EMAIL: str = "bilfordderek917@gmail.com"
    COMPANY_PHONE: str = "+254722206805"
    COMPANY_WEBSITE: str = "https://www.triventatech.com"
    COMPANY_LOCATION: str = "Nairobi, Kenya"
    SERVICES: str = "Web Development,AI & Data Science,Cybersecurity,Cloud Solutions,Mobile Apps,Training"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def services_list(self) -> List[str]:
        """Parse SERVICES into a list"""
        return [service.strip() for service in self.SERVICES.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
