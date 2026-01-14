# drop-table-regrets

A Python/PostgreSQL playground for learning, benchmarking, and making questionable schema decisions.

## Quick start

1. Install Python dependencies (from the project root).
2. Copy `.env.example` to `.env` and set `DATABASE_DSN` to point at your PostgreSQL database.
3. Create the `hello` table in your database via Alembic.
4. Run the demo script.

```bash
# 1. Install dependencies
pip install -e .

# 2. Configure environment
cp .env.example .env
# then edit .env and set DATABASE_DSN, for example:
# DATABASE_DSN=postgresql+psycopg://user:password@localhost:5432/drop_table_regrets
# Note: Alembic expects a SQLAlchemy URL (postgresql+psycopg://) while
# the app accepts plain psycopg URLs (postgresql://). Either works here.

# 3. Initialize database schema
alembic upgrade head

# 4. Run the demo script
python -m drop_table_regrets.run

# (Optional) Tear down schema
alembic downgrade base

# (Optional) Convenience commands
# make migrate
# make downgrade
```

## Makefile shortcuts

If you prefer, the Makefile wraps the common Alembic commands:

```bash
make migrate   # alembic upgrade head
make downgrade # alembic downgrade base
```
