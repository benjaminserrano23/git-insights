# Git Insights

CLI tool + HTML report that analyzes the history of any git repository. Extracts contribution stats, file hotspots, commit activity patterns, and codebase growth over time.

## Features

- **Contributions by author** — commits, lines added/deleted, files touched
- **File hotspots** — most frequently modified files (potential technical debt)
- **Commit activity heatmap** — when do commits happen? (by day of week and hour)
- **Codebase timeline** — cumulative lines of code over time
- **HTML report** — self-contained file with Chart.js graphs, dark theme
- **Console output** — Rich-formatted tables in the terminal

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Analyze current directory
python -m git_insights

# Analyze a specific repo
python -m git_insights /path/to/repo

# Generate HTML report
python -m git_insights /path/to/repo --html report.html
```

## Development

```bash
# Run tests
python -m pytest tests/ -v
```

## How it works

1. **GitPython** reads the commit history from the local `.git` directory
2. Each commit is analyzed for author, diffs (additions/deletions), and timestamps
3. **pandas** aggregates the data into DataFrames for each analysis dimension
4. **Rich** renders formatted tables in the terminal
5. **Jinja2** generates an HTML report with **Chart.js** graphs embedded inline

## Output example

```
┌─── Git Insights Report ────┐
│ my-project                 │
└────────────────────────────┘

📊 Summary
   Commits:      142
   Authors:      3
   First commit: 2024-01-15
   Last commit:  2026-04-06

          👥 Contributions by Author
┌─────────┬─────────┬───────────┬───────────┬───────┐
│ Author  │ Commits │ Additions │ Deletions │ Files │
├─────────┼─────────┼───────────┼───────────┼───────┤
│ Alice   │      89 │    +12340 │     -4521 │   156 │
│ Bob     │      42 │     +5670 │     -2340 │    87 │
│ Charlie │      11 │     +1230 │      -450 │    34 │
└─────────┴─────────┴───────────┴───────────┴───────┘
```

## Tech stack

- Python
- GitPython (git history access)
- pandas (data aggregation)
- Jinja2 (HTML templating)
- Chart.js (graphs in HTML report)
- Rich (terminal output)
- pytest (testing)
