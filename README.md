# drop-table-regrets
A Python/PostgreSQL playground for learning, benchmarking, and making questionable schema decisions.

## Quick start

1. Install Python dependencies (from the project root).
2. Copy `.env.example` to `.env` and set `DATABASE_DSN` to point at your PostgreSQL database.
3. Create the `hello` table in your database.
4. Run the demo script.

```bash
# 1. Install dependencies
pip install -e .

# 2. Configure environment
cp .env.example .env
# then edit .env and set DATABASE_DSN, for example:
# DATABASE_DSN=postgresql://user:password@localhost:5432/drop_table_regrets

# 3. Initialize database schema (run in psql against DATABASE_DSN)
psql "$DATABASE_DSN" <<'SQL'
CREATE TABLE IF NOT EXISTS hello (
    id   serial PRIMARY KEY,
    name text NOT NULL
);
SQL

# 4. Run the demo script
python -m drop_table_regrets.run
```
