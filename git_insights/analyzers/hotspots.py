"""Detect file hotspots — files modified most frequently."""

from collections import Counter
from git import Repo
import pandas as pd


def analyze_hotspots(repo: Repo, top_n: int = 20) -> pd.DataFrame:
    """Return a DataFrame of most frequently modified files."""
    file_changes: Counter[str] = Counter()
    file_authors: dict[str, set[str]] = {}

    for commit in repo.iter_commits("HEAD"):
        author = commit.author.name or "Unknown"
        try:
            if commit.parents:
                diffs = commit.parents[0].diff(commit)
            else:
                diffs = commit.diff(None)

            for diff in diffs:
                path = diff.b_path or diff.a_path or ""
                if path:
                    file_changes[path] += 1
                    if path not in file_authors:
                        file_authors[path] = set()
                    file_authors[path].add(author)
        except Exception:
            pass

    rows = []
    for path, count in file_changes.most_common(top_n):
        rows.append(
            {
                "file": path,
                "changes": count,
                "authors": len(file_authors.get(path, set())),
            }
        )

    return pd.DataFrame(rows)
