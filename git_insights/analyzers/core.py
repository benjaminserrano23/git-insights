"""Core analysis orchestrator."""

from dataclasses import dataclass
from git import Repo
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


def run_analysis(repo_path: str) -> AnalysisResult:
    """Run all analyses on the given repo path."""
    repo = Repo(repo_path)
    assert not repo.bare, "Cannot analyze a bare repository"

    commits = list(repo.iter_commits("HEAD"))
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
        contributions=analyze_contributions(repo),
        hotspots=analyze_hotspots(repo),
        activity=analyze_activity(repo),
        timeline=analyze_timeline(repo),
    )
