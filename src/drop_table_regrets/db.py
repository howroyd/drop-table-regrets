from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any, Protocol, runtime_checkable

import psycopg


@runtime_checkable
class CursorProtocol(Protocol):
    def __enter__(self) -> CursorProtocol: ...

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool: ...

    def execute(self, query: str, params: Sequence[Any] | None = None) -> Any: ...

    def fetchone(self) -> Any | None: ...

    def fetchall(self) -> list[Any]: ...


@runtime_checkable
class ConnectionProtocol(Protocol):
    def __enter__(self) -> ConnectionProtocol: ...

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool: ...

    def cursor(self) -> CursorProtocol: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


def connect(dsn: str) -> ConnectionProtocol:
    return psycopg.connect(dsn)  # type: ignore[return-value]


@contextmanager
def transaction(conn: ConnectionProtocol) -> Iterator[CursorProtocol]:
    with conn.cursor() as cur:
        try:
            yield cur
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
