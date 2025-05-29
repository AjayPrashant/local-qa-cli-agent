from app.loader import load_documents
from app.embedder import chunk_text, build_faiss_index
from app.qa_agent import answer_question
from rich.console import Console
from rich.prompt import Prompt
import sys

def run_indexing(console):
    console.print("[bold green]Local QA Agent - Index Builder[/bold green]")

    docs = load_documents("docs")
    if not docs:
        console.print("[yellow]No documents found to index.[/yellow]")
        sys.exit()

    console.print(f"Loaded {len(docs)} documents. Chunking...")
    chunks = chunk_text(docs)
    console.print(f"Created {len(chunks)} chunks. Generating embeddings...")

    build_faiss_index(chunks)

def run_qa(console):
    console.print("[bold blue]Local QA Agent - Ask Me Anything[/bold blue]")
    console.print("[dim]Type 'exit' to quit.[/dim]")

    while True:
        query = Prompt.ask("\n[bold]>[/bold]")
        if query.strip().lower() in {"exit", "quit"}:
            break
        answer = answer_question(query)
        console.print(f"[green]Answer:[/green] {answer}")

def main():
    console = Console()
    if "--qa" in sys.argv:
        run_qa(console)
    else:
        run_indexing(console)

if __name__ == "__main__":
    main()
