from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from drop_table_regrets.db import CursorProtocol


class Hello(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: int
    created_at: datetime
    msg: str


def create(cur: CursorProtocol, msg: str) -> Hello:
    cur.execute("INSERT INTO hello (msg) VALUES (%s) RETURNING id, created_at", (msg,))
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Failed to insert new record into hello table.")
    hello_id, created_at = row
    return Hello(id=hello_id, created_at=created_at, msg=msg)


def get(cur: CursorProtocol, hello_id: int) -> Hello | None:
    cur.execute("SELECT id, created_at, msg FROM hello WHERE id = %s", (hello_id,))
    row = cur.fetchone()
    if row is None:
        return None
    row_id, created_at, msg = row
    return Hello(id=row_id, created_at=created_at, msg=msg)


def update(cur: CursorProtocol, hello_id: int, msg: str) -> Hello | None:
    cur.execute(
        "UPDATE hello SET msg = %s WHERE id = %s RETURNING id, created_at, msg",
        (msg, hello_id),
    )
    row = cur.fetchone()
    if row is None:
        return None
    row_id, created_at, updated_msg = row
    return Hello(id=row_id, created_at=created_at, msg=updated_msg)


def delete(cur: CursorProtocol, hello_id: int) -> bool:
    cur.execute("DELETE FROM hello WHERE id = %s RETURNING id", (hello_id,))
    row = cur.fetchone()
    return row is not None


def list_all(cur: CursorProtocol, limit: int = 100, offset: int = 0) -> list[Hello]:
    cur.execute(
        "SELECT id, created_at, msg FROM hello ORDER BY id LIMIT %s OFFSET %s",
        (limit, offset),
    )
    rows = cur.fetchall()
    return [Hello(id=row_id, created_at=created_at, msg=msg) for row_id, created_at, msg in rows]
