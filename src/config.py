"""Configuration management for the therapy evaluation system."""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """System configuration."""
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY"
    )
    MODEL: str = "gpt-4.1-mini-2025-04-14"
    
    # Conversation settings
    CONVERSATION_TURNS: int = 5
    MAX_CONCURRENT_CONVERSATIONS: int = 10
    
    # Output settings
    RESULTS_DIR: str = "data/results"
    
    # Therapist settings
    THERAPIST_MAX_WORDS: int = 120
    
    # Timeout settings
    API_TIMEOUT: int = 30  # seconds
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Create results directory if it doesn't exist
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)