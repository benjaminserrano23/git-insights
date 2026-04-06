"""Console reporter using Rich."""

import io
import sys

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..analyzers.core import AnalysisResult


def print_report(result: AnalysisResult) -> None:
    """Print analysis results to the console."""
    # Force UTF-8 output on Windows to support emojis
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    console = Console(force_terminal=True)

    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]{result.repo_name}[/bold cyan]",
            title="Git Insights Report",
            border_style="cyan",
        )
    )
    console.print()

    # Summary
    console.print("[bold]📊 Summary[/bold]")
    console.print(f"   Commits:      {result.total_commits}")
    console.print(f"   Authors:      {result.total_authors}")
    console.print(f"   First commit: {result.first_commit_date}")
    console.print(f"   Last commit:  {result.last_commit_date}")
    console.print()

    # Contributions table
    if not result.contributions.empty:
        table = Table(title="👥 Contributions by Author", border_style="dim")
        table.add_column("Author", style="white")
        table.add_column("Commits", justify="right", style="cyan")
        table.add_column("Additions", justify="right", style="green")
        table.add_column("Deletions", justify="right", style="red")
        table.add_column("Files", justify="right", style="yellow")

        for _, row in result.contributions.iterrows():
            table.add_row(
                str(row["author"]),
                str(row["commits"]),
                f"+{row['additions']}",
                f"-{row['deletions']}",
                str(row["files_touched"]),
            )
        console.print(table)
        console.print()

    # Hotspots
    if not result.hotspots.empty:
        table = Table(title="🔥 File Hotspots (most modified)", border_style="dim")
        table.add_column("File", style="white")
        table.add_column("Changes", justify="right", style="yellow")
        table.add_column("Authors", justify="right", style="cyan")

        for _, row in result.hotspots.head(15).iterrows():
            table.add_row(
                str(row["file"]),
                str(row["changes"]),
                str(row["authors"]),
            )
        console.print(table)
        console.print()
