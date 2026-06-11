from pathlib import Path

from src.common.db import connect, init_db


def test_init_db_creates_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.sqlite"
    init_db(db_path)
    conn = connect(db_path)
    row = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runs'").fetchone()
    conn.close()
    assert row is not None
