"""CLI entry point for git-insights."""

import argparse
import sys

from .analyzers.core import run_analysis
from .reporters.console import print_report
from .reporters.html import generate_html


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

    args = parser.parse_args()

    try:
        result = run_analysis(args.repo)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print_report(result)

    if args.html:
        generate_html(result, args.html)
        print(f"\nHTML report saved to {args.html}")


if __name__ == "__main__":
    main()
