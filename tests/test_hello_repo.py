from __future__ import annotations

from datetime import datetime, timezone

import pytest

from drop_table_regrets.repos import hello


class FakeCursor:
    def __init__(self) -> None:
        self._next_result: tuple | None = None
        self._next_results: list[tuple] = []
        self._next_id = 1
        self._rows: dict[int, tuple[datetime, str]] = {}

    def execute(self, query: str, params: tuple | None = None) -> None:
        params = params or ()
        normalized = query.strip().upper()

        if normalized.startswith("INSERT"):
            msg = params[0]
            created_at = datetime(1970, 1, 1, tzinfo=timezone.utc)
            row_id = self._next_id
            self._next_id += 1
            self._rows[row_id] = (created_at, msg)
            self._next_result = (row_id, created_at)
            return

        if normalized.startswith("SELECT") and "WHERE ID" in normalized:
            row_id = params[0]
            row = self._rows.get(row_id)
            if row is None:
                self._next_result = None
            else:
                created_at, msg = row
                self._next_result = (row_id, created_at, msg)
            return

        if normalized.startswith("SELECT") and "ORDER BY" in normalized:
            limit, offset = params
            rows = []
            for row_id in sorted(self._rows):
                created_at, msg = self._rows[row_id]
                rows.append((row_id, created_at, msg))
            self._next_results = rows[offset : offset + limit]
            return

        if normalized.startswith("UPDATE"):
            msg, row_id = params
            row = self._rows.get(row_id)
            if row is None:
                self._next_result = None
            else:
                created_at, _ = row
                self._rows[row_id] = (created_at, msg)
                self._next_result = (row_id, created_at, msg)
            return

        if normalized.startswith("DELETE"):
            row_id = params[0]
            if row_id in self._rows:
                del self._rows[row_id]
                self._next_result = (row_id,)
            else:
                self._next_result = None
            return

        raise AssertionError(f"Unexpected query executed: {query}")

    def fetchone(self) -> tuple | None:
        result = self._next_result
        self._next_result = None
        return result

    def fetchall(self) -> list[tuple]:
        results = self._next_results
        self._next_results = []
        return results


class FakeCursorNoInsertReturn:
    def execute(self, query: str, params: tuple | None = None) -> None:
        return None

    def fetchone(self) -> tuple | None:
        return None


def test_crud_cycle() -> None:
    cur = FakeCursor()

    created = hello.create(cur, "hello")
    fetched = hello.get(cur, created.id)
    assert fetched == created

    updated = hello.update(cur, created.id, "updated")
    assert updated is not None
    assert updated.msg == "updated"

    deleted = hello.delete(cur, created.id)
    assert deleted is True
    assert hello.get(cur, created.id) is None


def test_update_missing_returns_none() -> None:
    cur = FakeCursor()
    assert hello.update(cur, 999, "missing") is None


def test_delete_missing_returns_false() -> None:
    cur = FakeCursor()
    assert hello.delete(cur, 999) is False


def test_list_all_with_pagination() -> None:
    cur = FakeCursor()
    hello.create(cur, "a")
    hello.create(cur, "b")
    hello.create(cur, "c")

    rows = hello.list_all(cur, limit=2, offset=1)
    assert [row.msg for row in rows] == ["b", "c"]


def test_create_raises_when_insert_returns_none() -> None:
    cur = FakeCursorNoInsertReturn()

    with pytest.raises(RuntimeError):
        hello.create(cur, "nope")
