"""Core analysis orchestrator."""

from dataclasses import dataclass
from datetime import datetime
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
import pandas as pd

from .contributions import analyze_contributions
from .hotspots import analyze_hotspots
from .activity import analyze_activity, analyze_timeline


@dataclass
class AnalysisResult:
    repo_name: str
    total_commits: int
    total_authors: int
    first_commit_date: str
    last_commit_date: str
    contributions: pd.DataFrame
    hotspots: pd.DataFrame
    activity: pd.DataFrame
    timeline: pd.DataFrame


def run_analysis(
    repo_path: str,
    since: str | None = None,
    author: str | None = None,
) -> AnalysisResult:
    """Run all analyses on the given repo path.

    Args:
        repo_path: Path to the git repository.
        since: Only include commits after this date (YYYY-MM-DD).
        author: Only include commits by this author (substring match).
    """
    try:
        repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise ValueError(f"Invalid git repository: {repo_path}") from e

    if repo.bare:
        raise ValueError("Cannot analyze a bare repository")

    commits = list(repo.iter_commits("HEAD"))

    # Apply filters
    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d")
            commits = [c for c in commits if c.authored_datetime.replace(tzinfo=None) >= since_date]
        except ValueError:
            raise ValueError(f"Invalid date format: {since}. Use YYYY-MM-DD.")

    if author:
        author_lower = author.lower()
        commits = [c for c in commits if author_lower in (c.author.name or "").lower()]

    total_commits = len(commits)
    authors = {c.author.name for c in commits}

    first_date = commits[-1].authored_datetime.strftime("%Y-%m-%d") if commits else "N/A"
    last_date = commits[0].authored_datetime.strftime("%Y-%m-%d") if commits else "N/A"

    repo_name = repo.working_dir.replace("\\", "/").split("/")[-1] if repo.working_dir else "unknown"

    return AnalysisResult(
        repo_name=repo_name,
        total_commits=total_commits,
        total_authors=len(authors),
        first_commit_date=first_date,
        last_commit_date=last_date,
        contributions=analyze_contributions(repo, commits),
        hotspots=analyze_hotspots(repo, commits),
        activity=analyze_activity(repo, commits),
        timeline=analyze_timeline(repo, commits),
    )
