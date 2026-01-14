# Copilot Instructions for drop-table-regrets

## Project Overview

This is a Python/PostgreSQL playground for learning, benchmarking, and making questionable schema decisions. The project uses Python 3.11+ with psycopg3 for database connectivity.

## Development Environment Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- pip package manager

### Installation
```bash
# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env and set DATABASE_DSN, for example:
# DATABASE_DSN=postgresql://user:password@localhost:5432/drop_table_regrets

# Initialize database schema (run in psql against DATABASE_DSN)
psql "$DATABASE_DSN" <<'SQL'
CREATE TABLE IF NOT EXISTS hello (
    id         serial PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT NOW(),
    msg        text NOT NULL
);
SQL
```

## Code Quality and Standards

### Linting
```bash
# Run ruff linter
ruff check .

# Fix auto-fixable issues
ruff check . --fix
```

### Type Checking
```bash
# Run mypy type checker
mypy src/drop_table_regrets --ignore-missing-imports
```

### Testing
```bash
# Run tests with pytest
pytest

# Run tests with verbose output
pytest -v
```

### Building
```bash
# Build distribution packages
python -m build
```

## Coding Conventions

### Python Style
- **Line length**: Maximum 100 characters (configured in pyproject.toml)
- **Target version**: Python 3.11
- **Type hints**: All functions must have type annotations (enforced by mypy with `disallow_untyped_defs`)
- **Import sorting**: Use isort style (handled by ruff)

### Code Quality Rules
The project uses ruff with the following enabled rule sets:
- `E`: pycodestyle errors
- `W`: pycodestyle warnings
- `F`: pyflakes
- `I`: isort (import sorting)
- `B`: flake8-bugbear (common bugs and design problems)
- `C4`: flake8-comprehensions (comprehension improvements)
- `UP`: pyupgrade (modern Python syntax)

### Testing Conventions
- Test files: `test_*.py` in the `tests/` directory
- Test functions: Must start with `test_`
- Use pytest fixtures for setup/teardown
- Mock external dependencies (e.g., database connections) using custom fake classes or pytest-mock

### Database Conventions
- Use psycopg (version 3.1+) for PostgreSQL connectivity
- Use context managers for connections and cursors
- Use parameterized queries to prevent SQL injection
- Load database DSN from `.env` file using python-dotenv

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── src/
│   └── drop_table_regrets/
│       └── run.py              # Main application entry point
├── tests/
│   └── test_run.py             # Tests for run.py
├── .env.example                # Example environment configuration
├── pyproject.toml              # Project metadata and tool configuration
├── requirements.txt            # Production dependencies
└── README.md                   # Project documentation
```

## Common Tasks

### Running the Application
```bash
# Run as a module
python -m drop_table_regrets.run

# Or use the installed console script
drop-table-regrets
```

### Adding Dependencies
1. Add to `requirements.txt` for production dependencies
2. Add to `pyproject.toml` under `[project.optional-dependencies]` for development dependencies
3. Run `pip install -e ".[dev]"` to install

## CI/CD

The project uses GitHub Actions for continuous integration:
- Runs on Python 3.11, 3.12, 3.13, and 3.14
- Executes linting (ruff), type checking (mypy), and tests (pytest)
- Builds distribution packages
- Triggered on pushes to `main` and pull requests

## Important Notes

- The project uses GPL-2.0-only license
- Environment variables are loaded from `.env` file (not committed to git)
- Database schema must be initialized manually before running the application
- Type checking with mypy is optional in CI but recommended locally
