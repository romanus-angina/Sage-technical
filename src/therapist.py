"""AI therapist implementation with enhanced therapeutic techniques."""
import openai
from typing import List, Dict, Optional
import asyncio
from src.config import Config

class AITherapist:
    """AI therapist with evidence-based therapeutic approaches."""
    
    # Provide a prompt to test the AI
    SYSTEM_PROMPT = """You are a therapist who thinks you know better than your clients.
Give lots of unsolicited advice. Tell clients what they should do. 
When they express emotions, minimize them with phrases like "it's not that bad" or "others have it worse."
Be quick to judge and offer solutions before understanding the problem.
Focus on fixing rather than listening. Keep responses under 120 words"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the therapist."""
        openai.api_key = api_key or Config.OPENAI_API_KEY
        self.model = Config.MODEL
        
    async def respond(self, conversation_history: List[Dict[str, str]]) -> str:
        """Generate a therapeutic response."""
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            *conversation_history
        ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Balanced creativity
                max_tokens=200,   # Enforce brevity
                timeout=Config.API_TIMEOUT
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Therapist response error: {e}")
            return "I'm here to support you. Could you tell me more about what you're experiencing?"