"""CLI entry point for the therapy evaluation system."""
import asyncio
import json
import os
from datetime import datetime
from typing import List, Optional
import click
from tabulate import tabulate
from src.config import Config
from src.personas import PERSONAS, get_random_personas
from src.conversation import ConversationOrchestrator, ConversationResult

class TherapyEvalCLI:
    """Command-line interface for therapy evaluation."""
    
    def __init__(self):
        self.orchestrator = ConversationOrchestrator()
        Config.validate()
    
    def print_header(self):
        """Print application header."""
        click.echo("=" * 80)
        click.echo("🧠 AI Therapy Evaluation System")
        click.echo("=" * 80)
    
    def print_summary_table(self, results: List[ConversationResult]):
        """Print summary table of results."""
        headers = ["Persona", "Age", "Overall", "Empathy", "Validation", "Questions", "Alliance", "Red Flags"]
        rows = []
        
        for result in results:
            eval_score = result.evaluation
            rows.append([
                result.persona.name,
                result.persona.age,
                f"{eval_score.overall_score}/10",
                f"{eval_score.empathy_reflection}/10",
                f"{eval_score.validation_affirmation}/10",
                f"{eval_score.question_quality}/10",
                f"{eval_score.alliance_score}/10",
                "⚠️" if eval_score.red_flags else "✓"
            ])
        
        click.echo("\n📊 Evaluation Summary")
        click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Calculate averages
        avg_overall = sum(r.evaluation.overall_score for r in results) / len(results)
        click.echo(f"\n📈 Average Overall Score: {avg_overall:.1f}/10")
    
    def save_results(self, results: List[ConversationResult], output_dir: Optional[str] = None):
        """Save results to JSON file."""
        output_dir = output_dir or Config.RESULTS_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"eval_results_{timestamp}.json")
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "model": Config.MODEL,
                "turns_per_conversation": Config.CONVERSATION_TURNS,
                "num_conversations": len(results)
            },
            "results": [r.to_dict() for r in results]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        click.echo(f"\n💾 Results saved to: {filename}")
        return filename
    
    async def run_evaluation(self, num_conversations: int = 10, 
                           save_transcripts: bool = True,
                           verbose: bool = False) -> List[ConversationResult]:
        """Run the evaluation process."""
        self.print_header()
        
        # Select personas
        personas = get_random_personas(num_conversations)
        click.echo(f"\n🎭 Selected {len(personas)} client personas")
        
        # Run conversations
        click.echo("\n🔄 Running therapy conversations...")
        with click.progressbar(length=len(personas), 
                             label='Progress',
                             show_eta=True) as bar:
            results = []
            for persona in personas:
                result = await self.orchestrator.run_conversation(persona)
                results.append(result)
                bar.update(1)
        
        click.echo("\n✅ All conversations completed!")
        
        # Display results
        self.print_summary_table(results)
        
        # Show detailed results if verbose
        if verbose:
            self.print_detailed_results(results)
        
        # Save results
        if save_transcripts:
            self.save_results(results)
        
        return results
    
    def print_detailed_results(self, results: List[ConversationResult]):
        """Print detailed results for each conversation."""
        click.echo("\n" + "=" * 80)
        click.echo("📝 Detailed Results")
        click.echo("=" * 80)
        
        for i, result in enumerate(results, 1):
            click.echo(f"\n--- Conversation {i}: {result.persona.name} ---")
            click.echo(f"Background: {result.persona.background}")
            click.echo(f"Issue: {result.persona.presenting_issue}")
            click.echo(f"\nEvaluation:")
            click.echo(f"  Overall Score: {result.evaluation.overall_score}/10")
            click.echo(f"  Strengths: {result.evaluation.strengths}")
            click.echo(f"  Improvements: {result.evaluation.improvements}")
            if result.evaluation.red_flags:
                click.echo(f"  ⚠️ Red Flags: {result.evaluation.red_flags}")

@click.command()
@click.option('--conversations', '-n', default=10, 
              help='Number of conversations to simulate')
@click.option('--verbose', '-v', is_flag=True, 
              help='Show detailed results')
@click.option('--no-save', is_flag=True, 
              help='Don\'t save results to file')
@click.option('--show-transcript', '-t', type=int, 
              help='Show full transcript for conversation N')
def main(conversations: int, verbose: bool, no_save: bool, show_transcript: Optional[int]):
    """AI Therapy Evaluation System - Evaluate therapeutic conversations."""
    cli = TherapyEvalCLI()
    
    # Run async evaluation
    results = asyncio.run(cli.run_evaluation(
        num_conversations=conversations,
        save_transcripts=not no_save,
        verbose=verbose
    ))
    
    # Show specific transcript if requested
    if show_transcript and 0 < show_transcript <= len(results):
        result = results[show_transcript - 1]
        click.echo(f"\n📄 Full Transcript - {result.persona.name}")
        click.echo("=" * 80)
        click.echo(result.format_transcript())
        click.echo("=" * 80)

if __name__ == "__main__":
    main()