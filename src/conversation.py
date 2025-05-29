"""Orchestrates therapy conversations."""
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from src.personas import Persona
from src.therapist import AITherapist
from src.client import ClientSimulator
from src.evaluator import ConversationEvaluator, EvaluationScore
from src.config import Config

class ConversationResult:
    """Results of a single therapy conversation."""
    
    def __init__(self, persona: Persona, transcript: List[Dict[str, str]], 
                 evaluation: EvaluationScore, duration: float):
        self.persona = persona
        self.transcript = transcript
        self.evaluation = evaluation
        self.duration = duration
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "persona": {
                "name": self.persona.name,
                "age": self.persona.age,
                "background": self.persona.background,
                "presenting_issue": self.persona.presenting_issue
            },
            "transcript": self.transcript,
            "evaluation": self.evaluation.to_dict(),
            "duration_seconds": self.duration,
            "timestamp": self.timestamp.isoformat()
        }
    
    def format_transcript(self) -> str:
        """Format transcript for display."""
        lines = []
        for i, msg in enumerate(self.transcript):
            role = "CLIENT" if msg["role"] == "user" else "THERAPIST"
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines)

class ConversationOrchestrator:
    """Orchestrates therapy conversations and evaluations."""
    
    def __init__(self):
        self.therapist = AITherapist()
        self.evaluator = ConversationEvaluator()
    
    async def run_conversation(self, persona: Persona) -> ConversationResult:
        """Run a complete therapy conversation."""
        start_time = datetime.now()
        client = ClientSimulator(persona)
        conversation_history = []
        
        # Run conversation turns
        for turn in range(Config.CONVERSATION_TURNS):
            # Client message
            client_msg = await client.generate_message(conversation_history)
            conversation_history.append({"role": "user", "content": client_msg})
            
            # Therapist response
            therapist_msg = await self.therapist.respond(conversation_history)
            conversation_history.append({"role": "assistant", "content": therapist_msg})
        
        # Format transcript for evaluation
        transcript = self._format_for_evaluation(conversation_history)
        
        # Evaluate conversation
        evaluation = await self.evaluator.evaluate(transcript)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        return ConversationResult(persona, conversation_history, evaluation, duration)
    
    def _format_for_evaluation(self, history: List[Dict[str, str]]) -> str:
        """Format conversation for evaluator."""
        lines = []
        for msg in history:
            role = "CLIENT" if msg["role"] == "user" else "THERAPIST"
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines)
    
    async def run_multiple_conversations(self, personas: List[Persona]) -> List[ConversationResult]:
        """Run multiple conversations in parallel."""
        # Limit concurrency to avoid rate limits
        semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT_CONVERSATIONS)
        
        async def run_with_semaphore(persona: Persona) -> ConversationResult:
            async with semaphore:
                return await self.run_conversation(persona)
        
        tasks = [run_with_semaphore(persona) for persona in personas]
        return await asyncio.gather(*tasks)