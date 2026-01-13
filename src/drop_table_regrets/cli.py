"""Command-line interface for drop-table-regrets."""

import argparse

from drop_table_regrets import __version__
from drop_table_regrets.example import greet


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="drop-table-regrets CLI",
        prog="drop-table-regrets",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"drop-table-regrets {__version__}",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)",
    )

    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
