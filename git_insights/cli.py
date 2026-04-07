"""CLI entry point for git-insights."""

import argparse
import sys

from .analyzers.core import run_analysis
from .reporters.console import print_report
from .reporters.html import generate_html
from .reporters.json_reporter import write_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="git-insights",
        description="Analyze git history and generate quality reports",
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    parser.add_argument(
        "--html",
        metavar="PATH",
        help="Generate an HTML report at the given path",
    )
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="Export results as JSON to the given path",
    )
    parser.add_argument(
        "--since",
        metavar="DATE",
        help="Only include commits after this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--author",
        metavar="NAME",
        help="Only include commits by this author (substring match)",
    )

    args = parser.parse_args()

    try:
        result = run_analysis(args.repo, since=args.since, author=args.author)
    except (ValueError, Exception) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print_report(result)

    if args.html:
        generate_html(result, args.html)
        print(f"\nHTML report saved to {args.html}")

    if args.json:
        write_json(result, args.json)
        print(f"\nJSON report saved to {args.json}")


if __name__ == "__main__":
    main()
