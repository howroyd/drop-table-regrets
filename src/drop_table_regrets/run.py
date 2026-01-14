from pathlib import Path

import dotenv
import psycopg

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
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO hello (msg) VALUES (%s) RETURNING id", ("from python",))

            next_record = cur.fetchone()
            if next_record is None:
                raise RuntimeError("Failed to insert new record into hello table.")
            new_id = next_record[0]

            cur.execute("SELECT id, created_at, msg FROM hello WHERE id = %s", (new_id,))
            row = cur.fetchone()
            print(row)


if __name__ == "__main__":
    main()
