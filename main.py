import sys
from pathlib import Path

# Ensure the root project directory is in python path
sys.path.append(str(Path(__file__).resolve().parent))

import click
from rich.console import Console
from rich.panel import Panel
from src.ai_client import AIBacklogClient
from src.parser import DocumentParser

console = Console(stderr=True)

@click.command()
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Path to input text, markdown, or PDF file.")
@click.option("--output-json", "-oj", default="outputs/backlog_result.json", help="Path to save output JSON backlog.")
@click.option("--output-html", "-oh", default="outputs/dashboard.html", help="Path to save interactive HTML dashboard view.")
@click.option("--autodelete", is_flag=True, help="Automatically delete input file after successful processing.")
def main(input, output_json, output_html, autodelete):
    """Smart Backlog Assistant CLI: Transform rough notes into structured user stories with JSON and Dashboard export."""
    console.print(Panel.fit("[bold cyan]Smart Backlog Assistant[/bold cyan]\n[italic]AI-Powered Agile Requirement Grooming (Gemini)[/italic]", border_style="cyan"))

    try:
        console.print(f"[yellow]Loading and parsing input file:[/yellow] {input}")
        raw_text = DocumentParser.load_file(input, auto_delete=autodelete)
        if autodelete:
            console.print(f"[dim red]Input file {input} was automatically deleted post-ingestion.[/dim red]")

        console.print(f"[yellow]Analyzing requirements with Google Gemini...[/yellow]")
        ai_client = AIBacklogClient()
        backlog_data = ai_client.generate_backlog(raw_text)

        # Save both structured JSON and executive HTML Dashboard view
        dump_data = backlog_data.model_dump()
        DocumentParser.save_output(dump_data, output_json)
        DocumentParser.save_html_dashboard(dump_data, output_html)
        
        console.print(f"\n[bold green]Success! Artifacts generated:[/bold green]")
        console.print(f"  - JSON Backlog: [cyan]{output_json}[/cyan]")
        console.print(f"  - HTML Dashboard View: [cyan]{output_html}[/cyan]")
        console.print(f"[cyan]Total User Stories Created:[/cyan] {len(backlog_data.user_stories)}")

    except Exception as e:
        console.print(f"\n[bold red]Error Execution Failed:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()