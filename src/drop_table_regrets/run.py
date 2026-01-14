from pathlib import Path

import dotenv
from rich import print as rich_print

from drop_table_regrets import db
from drop_table_regrets.repos import hello as hello_repo

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
DSN_KEY = "DATABASE_DSN"


def _load_dsn() -> str:
    """Load DATABASE_DSN from the project's .env file."""

    if not ENV_PATH.exists():
        raise FileNotFoundError(f"Database configuration file not found: {ENV_PATH}")

    dsn = dotenv.dotenv_values(ENV_PATH).get(DSN_KEY)
    if not dsn:
        raise ValueError(f"{DSN_KEY} is not set in {ENV_PATH}")

    if dsn.startswith("postgresql+psycopg://"):
        return dsn.replace("postgresql+psycopg://", "postgresql://", 1)

    return dsn


def main() -> None:
    dsn = _load_dsn()
    with db.connect(dsn) as conn:
        with db.transaction(conn) as cur:
            created = hello_repo.create(cur, "from python")

        with db.transaction(conn) as cur:
            row = hello_repo.get(cur, created.id)
            rich_print(row)


if __name__ == "__main__":
    main()
