"""Client simulator for realistic therapy conversations."""
import openai
from typing import List, Dict, Optional
import asyncio
from src.config import Config
from src.personas import Persona

class ClientSimulator:
    """Simulates realistic client responses in therapy."""
    
    def __init__(self, persona: Persona, api_key: Optional[str] = None):
        """Initialize with a specific persona."""
        self.persona = persona
        openai.api_key = api_key or Config.OPENAI_API_KEY
        self.model = Config.MODEL
        self.turn_count = 0
        
    def _get_turn_guidance(self) -> str:
        """Provide turn-specific guidance for realistic progression."""
        if self.turn_count == 0:
            return "This is your first message. Introduce your main concern naturally."
        elif self.turn_count == 1:
            return "Share more details about your situation. You're still testing the waters."
        elif self.turn_count == 2:
            return "You're starting to trust more. Share a specific example or deeper feeling."
        elif self.turn_count == 3:
            return "Reflect on what the therapist has said. Show some insight or resistance."
        else:
            return "This is your final message. Express how you're feeling about the conversation."
    
    async def generate_message(self, conversation_history: List[Dict[str, str]]) -> str:
        """Generate next client message."""
        turn_guidance = self._get_turn_guidance()
        
        messages = [
            {"role": "system", "content": f"{self.persona.system_prompt}\n\n{turn_guidance}"},
            *conversation_history,
            {"role": "assistant", "content": "(You think about what to share and then respond as the client)"}
        ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.8,  # More variation in client responses
                max_tokens=150,
                timeout=Config.API_TIMEOUT
            )
            self.turn_count += 1
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Client simulator error: {e}")
            return "I'm not sure how to express what I'm feeling right now."