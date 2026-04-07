"""JSON reporter — exports analysis results to a JSON file."""

import json
from pathlib import Path

from ..analyzers.core import AnalysisResult


def write_json(result: AnalysisResult, output_path: str) -> None:
    """Serialize analysis results to a JSON file."""
    data = {
        "repo_name": result.repo_name,
        "total_commits": result.total_commits,
        "total_authors": result.total_authors,
        "first_commit_date": result.first_commit_date,
        "last_commit_date": result.last_commit_date,
        "contributions": result.contributions.to_dict("records") if not result.contributions.empty else [],
        "hotspots": result.hotspots.to_dict("records") if not result.hotspots.empty else [],
        "activity": result.activity[result.activity["commits"] > 0].to_dict("records") if not result.activity.empty else [],
        "timeline": result.timeline.to_dict("records") if not result.timeline.empty else [],
    }

    Path(output_path).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
