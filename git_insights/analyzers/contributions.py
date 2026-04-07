"""Analyze per-author contributions from git history."""

from collections import defaultdict
from git import Repo, Commit
import pandas as pd


def analyze_contributions(repo: Repo, commits: list[Commit] | None = None) -> pd.DataFrame:
    """Return a DataFrame with per-author contribution stats."""
    if commits is None:
        commits = list(repo.iter_commits("HEAD"))

    stats: dict[str, dict] = defaultdict(
        lambda: {"commits": 0, "additions": 0, "deletions": 0, "files_touched": set()}
    )

    for commit in commits:
        author = commit.author.name or "Unknown"
        stats[author]["commits"] += 1

        try:
            if commit.parents:
                diffs = commit.parents[0].diff(commit)
            else:
                diffs = commit.diff(None)

            for diff in diffs:
                path = diff.b_path or diff.a_path or ""
                stats[author]["files_touched"].add(path)

                try:
                    text = diff.diff.decode("utf-8", errors="ignore") if diff.diff else ""
                    for line in text.splitlines():
                        if line.startswith("+") and not line.startswith("+++"):
                            stats[author]["additions"] += 1
                        elif line.startswith("-") and not line.startswith("---"):
                            stats[author]["deletions"] += 1
                except Exception:
                    pass
        except Exception:
            pass

    rows = []
    for author, data in stats.items():
        rows.append(
            {
                "author": author,
                "commits": data["commits"],
                "additions": data["additions"],
                "deletions": data["deletions"],
                "files_touched": len(data["files_touched"]),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("commits", ascending=False).reset_index(drop=True)
    return df
