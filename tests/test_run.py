"""Tests for drop_table_regrets.run using mocked database connections."""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest

from drop_table_regrets import run


class FakeCursor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Sequence[Any]]] = []
        self._next_result: tuple[Any, ...] | None = None
        self._last_id = 1
        self._last_message = "from python"

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # pragma: no cover - simple context plumbing
        return False

    def execute(self, query: str, params: Sequence[Any] | None = None) -> None:
        params = params or ()
        self.calls.append((query, tuple(params)))
        normalized = query.strip().upper()

        if normalized.startswith("INSERT"):
            self._last_message = params[0] if params else self._last_message
            self._next_result = (self._last_id,)
        elif normalized.startswith("SELECT"):
            self._next_result = (
                self._last_id,
                "1970-01-01T00:00:00Z",
                self._last_message,
            )
        else:
            raise AssertionError(f"Unexpected query executed: {query}")

    def fetchone(self) -> tuple[Any, ...]:
        if self._next_result is None:
            raise AssertionError("fetchone() called before execute()")

        result = self._next_result
        self._next_result = None
        return result


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursor()
        self.closed = False
        self.committed = False

    def __enter__(self) -> "FakeConnection":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # pragma: no cover - simple context plumbing
        if exc_type is None:
            self.commit()
        self.closed = True
        return False

    def cursor(self) -> FakeCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.committed = True


def test_load_dsn_reads_value_from_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("DATABASE_DSN=postgresql://local/test\n", encoding="utf-8")
    monkeypatch.setattr(run, "ENV_PATH", env_file)

    assert run._load_dsn() == "postgresql://local/test"


def test_load_dsn_missing_file_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    missing = tmp_path / "missing.env"
    monkeypatch.setattr(run, "ENV_PATH", missing)

    with pytest.raises(FileNotFoundError):
        run._load_dsn()


def test_load_dsn_missing_key_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("OTHER=value\n", encoding="utf-8")
    monkeypatch.setattr(run, "ENV_PATH", env_file)

    with pytest.raises(ValueError):
        run._load_dsn()


def test_main_uses_fake_connection(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_conn = FakeConnection()

    monkeypatch.setattr(run, "_load_dsn", lambda: "postgresql://fake")
    monkeypatch.setattr(run.psycopg, "connect", lambda dsn: fake_conn)

    run.main()

    out = capsys.readouterr().out
    assert "from python" in out
    assert fake_conn.cursor_obj.calls[0][0].strip().upper().startswith("INSERT")
    assert fake_conn.cursor_obj.calls[1][0].strip().upper().startswith("SELECT")
    assert fake_conn.committed is True
    assert fake_conn.closed is True
