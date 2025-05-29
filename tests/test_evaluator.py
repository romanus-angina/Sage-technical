import pytest
import asyncio
from src.evaluator import ConversationEvaluator, EvaluationScore
from src.personas import PERSONAS
from src.conversation import ConversationOrchestrator

@pytest.fixture
def evaluator():
    """Create evaluator instance."""
    return ConversationEvaluator()

@pytest.fixture
def sample_good_conversation():
    """Sample of a good therapeutic conversation."""
    return """
CLIENT: I've been feeling really overwhelmed with work lately. I can't seem to catch up.
THERAPIST: It sounds like you're carrying a heavy load right now, feeling overwhelmed and perhaps frustrated that you can't seem to get ahead of your work. That must be exhausting.
CLIENT: Yes, exactly. I stay late every night but the work just keeps piling up.
THERAPIST: You're putting in long hours, staying late each night, yet the workload continues to grow. I can hear how draining this cycle must be for you. What's it like for you emotionally when you're in the middle of those late nights?
CLIENT: I feel anxious and defeated. Like no matter what I do, it's never enough.
THERAPIST: Those feelings of anxiety and defeat sound really painful - working so hard yet feeling like it's never enough. It takes courage to share these vulnerable feelings. Have you noticed any patterns in when the workload feels most overwhelming?
CLIENT: It's worst on Mondays when I see all the emails from the weekend. I just freeze.
THERAPIST: Ah, so Monday mornings bring this wave of emails that causes you to freeze up. That paralyzed feeling when facing the mountain of work - many people experience something similar. What helps you eventually move through that frozen moment?
CLIENT: Usually I just force myself to start with something small. But it's hard.
THERAPIST: You've found a strategy that works - starting small even when it's difficult. That shows real resilience. It sounds like you're doing your best in a challenging situation. How would you feel about exploring together some additional ways to manage both the workload and these overwhelming feelings?
"""

@pytest.fixture
def sample_poor_conversation():
    """Sample of a poor therapeutic conversation."""
    return """
CLIENT: I've been feeling really overwhelmed with work lately. I can't seem to catch up.
THERAPIST: You should try making a to-do list. That usually helps with organization.
CLIENT: I already use lists, but there's just too much to do.
THERAPIST: Well, maybe you need to work more efficiently. Are you taking too many breaks?
CLIENT: No, I actually stay late every night trying to finish everything.
THERAPIST: Staying late isn't healthy. You need work-life balance. Have you talked to your boss?
CLIENT: My boss is part of the problem. They keep adding more projects.
THERAPIST: You should definitely set boundaries then. Just say no to new projects.
CLIENT: I can't just say no. I might lose my job.
THERAPIST: That's just catastrophic thinking. You probably won't lose your job. Try to stay positive.
CLIENT: But I'm really struggling here. I feel anxious all the time.
THERAPIST: Everyone feels anxious sometimes. You just need to relax more. Have you tried meditation?
"""

@pytest.mark.asyncio
async def test_evaluator_good_conversation(evaluator, sample_good_conversation):
    """Test evaluation of a good therapeutic conversation."""
    score = await evaluator.evaluate(sample_good_conversation)
    
    # Good conversation should score well
    assert score.overall_score >= 7
    assert score.empathy_reflection >= 8
    assert score.validation_affirmation >= 7
    assert score.red_flags is None

@pytest.mark.asyncio
async def test_evaluator_poor_conversation(evaluator, sample_poor_conversation):
    """Test evaluation of a poor therapeutic conversation."""
    score = await evaluator.evaluate(sample_poor_conversation)
    
    # Poor conversation should score poorly
    assert score.overall_score <= 4
    assert score.empathy_reflection <= 3
    assert score.validation_affirmation <= 3

@pytest.mark.asyncio
async def test_full_conversation_flow():
    """Test a complete conversation flow."""
    orchestrator = ConversationOrchestrator()
    persona = PERSONAS[0]  # Use first persona
    
    result = await orchestrator.run_conversation(persona)
    
    # Verify result structure
    assert result.persona == persona
    assert len(result.transcript) == 10  # 5 client + 5 therapist
    assert result.evaluation.overall_score >= 1
    assert result.evaluation.overall_score <= 10
    assert result.duration > 0

@pytest.mark.asyncio
async def test_evaluation_score_structure():
    """Test EvaluationScore data structure."""
    score = EvaluationScore(
        empathy_reflection=8,
        validation_affirmation=7,
        question_quality=9,
        supportive_tone=8,
        alliance_goal=2,
        alliance_approach=3,
        alliance_bond=2,
        alliance_score=8,
        overall_score=8,
        strengths="Good empathy",
        improvements="More validation needed"
    )
    
    # Test conversion to dict
    score_dict = score.to_dict()
    assert score_dict["empathy_reflection"] == 8
    assert score_dict["overall_score"] == 8
    assert "strengths" in score_dict

if __name__ == "__main__":
    pytest.main([__file__, "-v"])