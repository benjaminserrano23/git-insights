"""Console reporter using Rich."""

import io
import sys

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..analyzers.core import AnalysisResult

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def print_report(result: AnalysisResult) -> None:
    """Print analysis results to the console."""
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

    # Contributions
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

    # Activity — top 5 most active hours
    if not result.activity.empty:
        active = result.activity[result.activity["commits"] > 0].sort_values(
            "commits", ascending=False
        ).head(5)
        if not active.empty:
            console.print("[bold]⏰ Most Active Hours[/bold]")
            for _, row in active.iterrows():
                day = row["day"]
                hour = int(row["hour"])
                commits = int(row["commits"])
                console.print(f"   {day} {hour:02d}:00 — [cyan]{commits}[/cyan] commits")
            console.print()

    # Timeline — current codebase size
    if not result.timeline.empty:
        latest = result.timeline.iloc[-1]
        size = int(latest["cumulative_size"])
        console.print("[bold]📈 Codebase Size[/bold]")
        console.print(f"   ~{size:,} lines (cumulative net)")
        console.print()
