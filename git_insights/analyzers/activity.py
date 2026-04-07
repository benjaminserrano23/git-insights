"""Analyze commit activity patterns by hour and day of week."""

from collections import defaultdict
from git import Repo, Commit
import pandas as pd


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def analyze_activity(repo: Repo, commits: list[Commit] | None = None) -> pd.DataFrame:
    """Return a DataFrame with commit counts per (day_of_week, hour)."""
    if commits is None:
        commits = list(repo.iter_commits("HEAD"))

    heatmap: dict[tuple[int, int], int] = defaultdict(int)

    for commit in commits:
        dt = commit.authored_datetime
        heatmap[(dt.weekday(), dt.hour)] += 1

    rows = []
    for day_idx in range(7):
        for hour in range(24):
            rows.append(
                {
                    "day": DAYS[day_idx],
                    "day_index": day_idx,
                    "hour": hour,
                    "commits": heatmap.get((day_idx, hour), 0),
                }
            )

    return pd.DataFrame(rows)


def analyze_timeline(repo: Repo, commits: list[Commit] | None = None) -> pd.DataFrame:
    """Return a DataFrame with cumulative lines of code over time."""
    if commits is None:
        commits = list(repo.iter_commits("HEAD"))

    data: list[dict] = []

    for commit in commits:
        additions = 0
        deletions = 0
        try:
            if commit.parents:
                diffs = commit.parents[0].diff(commit)
            else:
                diffs = commit.diff(None)

            for diff in diffs:
                try:
                    text = diff.diff.decode("utf-8", errors="ignore") if diff.diff else ""
                    for line in text.splitlines():
                        if line.startswith("+") and not line.startswith("+++"):
                            additions += 1
                        elif line.startswith("-") and not line.startswith("---"):
                            deletions += 1
                except Exception:
                    pass
        except Exception:
            pass

        data.append(
            {
                "date": commit.authored_datetime.strftime("%Y-%m-%d"),
                "additions": additions,
                "deletions": deletions,
            }
        )

    df = pd.DataFrame(data)
    if df.empty:
        return df

    df = df.groupby("date").sum().sort_index().reset_index()
    df["net"] = df["additions"] - df["deletions"]
    df["cumulative_size"] = df["net"].cumsum()
    return df
