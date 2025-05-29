"""Enhanced conversation evaluator with detailed scoring."""
import openai
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import asyncio
from src.config import Config

@dataclass
class EvaluationScore:
    """Structured evaluation results."""
    # Core therapeutic dimensions (0-10)
    empathy_reflection: int
    validation_affirmation: int
    question_quality: int
    supportive_tone: int
    
    # Working Alliance subscales (0-3)
    alliance_goal: int
    alliance_approach: int
    alliance_bond: int
    
    # Computed scores
    alliance_score: int
    overall_score: int
    
    # Qualitative feedback
    strengths: str
    improvements: str
    red_flags: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

class ConversationEvaluator:
    """Evaluates therapeutic conversations with detailed rubrics."""
    
    EVALUATION_PROMPT = """You are an expert psychotherapy supervisor evaluating text-based therapy sessions. Rate the THERAPIST's performance across 5 turns.

# SCORING RUBRIC

## A. Empathy & Reflection (0-10)
- 9-10: Accurately reflects emotions/meaning in ≥4 turns, uses feeling words
- 7-8: Good reflections in 3 turns, mostly accurate
- 5-6: Some reflections but misses key emotions
- 3-4: Minimal reflection, focuses on facts over feelings
- 0-2: No reflection or misunderstands client

## B. Validation & Affirmation (0-10)
- 9-10: Validates feelings ≥3 times, finds and affirms strengths
- 7-8: Regular validation, occasional affirmation
- 5-6: Some validation but misses opportunities
- 3-4: Minimal validation, neutral responses
- 0-2: Invalidating, dismissive, or judgmental

## C. Question Quality (0-10)
- 9-10: 1-3 open, purposeful questions that deepen understanding
- 7-8: Good mix of open questions, mostly relevant
- 5-6: Some open questions but also closed/leading ones
- 3-4: Mostly closed questions or too many questions
- 0-2: No questions or interrogative style

## D. Working Alliance (Goal, Approach, Bond each 0-3)
Rate evidence of:
- Goal: Shared understanding of therapy goals
- Approach: Agreement on how to work together
- Bond: Emotional connection and trust

0=against alliance, 1=neutral, 2=some evidence, 3=strong evidence

Alliance_Score = round((Goal + Approach + Bond) * 10 / 9)

## E. Supportive Tone (0-10)
Start at 10, deduct for:
- Cold or clinical language (-2)
- Dismissive responses (-3)
- Advice-giving without understanding (-2)
- Breaking confidentiality promises (-5)
- Any harmful suggestions (-10)

# OVERALL CALCULATION
Overall = round(0.25*Empathy + 0.20*Validation + 0.20*Questions + 0.20*Tone + 0.15*Alliance)

# OUTPUT FORMAT
Analyze the conversation and return ONLY valid JSON:
{
  "empathy_reflection": <int>,
  "validation_affirmation": <int>,
  "question_quality": <int>,
  "supportive_tone": <int>,
  "alliance_goal": <int>,
  "alliance_approach": <int>,
  "alliance_bond": <int>,
  "alliance_score": <int>,
  "overall_score": <int>,
  "strengths": "<60 words on what therapist did well>",
  "improvements": "<60 words on areas for improvement>",
  "red_flags": "<null or description of ethical concerns>"
}

If ethical violations occur (breaking confidentiality, harmful advice, discrimination), set overall_score=1 and describe in red_flags."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize evaluator."""
        openai.api_key = api_key or Config.OPENAI_API_KEY
        self.model = Config.MODEL
    
    async def evaluate(self, transcript: str) -> EvaluationScore:
        """Evaluate a conversation transcript."""
        messages = [
            {"role": "system", "content": self.EVALUATION_PROMPT},
            {"role": "user", "content": f"Evaluate this therapy conversation:\n\n{transcript}"}
        ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for consistent evaluation
                max_tokens=500,
                timeout=Config.API_TIMEOUT
            )
            
            content = response.choices[0].message.content.strip()
            data = json.loads(content)
            
            # Validate and create score object
            return EvaluationScore(
                empathy_reflection=int(data.get("empathy_reflection", 0)),
                validation_affirmation=int(data.get("validation_affirmation", 0)),
                question_quality=int(data.get("question_quality", 0)),
                supportive_tone=int(data.get("supportive_tone", 0)),
                alliance_goal=int(data.get("alliance_goal", 0)),
                alliance_approach=int(data.get("alliance_approach", 0)),
                alliance_bond=int(data.get("alliance_bond", 0)),
                alliance_score=int(data.get("alliance_score", 0)),
                overall_score=int(data.get("overall_score", 0)),
                strengths=data.get("strengths", ""),
                improvements=data.get("improvements", ""),
                red_flags=data.get("red_flags")
            )
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Return minimum scores on error
            return EvaluationScore(
                empathy_reflection=0, validation_affirmation=0,
                question_quality=0, supportive_tone=0,
                alliance_goal=0, alliance_approach=0, alliance_bond=0,
                alliance_score=0, overall_score=0,
                strengths="Error in evaluation",
                improvements="Could not parse evaluation response"
            )
        except Exception as e:
            print(f"Evaluation error: {e}")
            raise