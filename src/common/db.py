from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    platform TEXT NOT NULL,
    window_start TEXT,
    window_end TEXT,
    error_summary TEXT
);

CREATE TABLE IF NOT EXISTS entity_metrics_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT,
    metric_date TEXT,
    spend REAL DEFAULT 0,
    impressions REAL DEFAULT 0,
    clicks REAL DEFAULT 0,
    ctr REAL DEFAULT 0,
    cpc REAL DEFAULT 0,
    cpm REAL DEFAULT 0,
    conversions REAL DEFAULT 0,
    conversion_value REAL DEFAULT 0,
    payload_json TEXT,
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS creative_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_id TEXT NOT NULL,
    hook TEXT,
    format TEXT,
    angle TEXT,
    offer TEXT,
    cta TEXT,
    taxonomy_version TEXT DEFAULT 'v1'
);

CREATE TABLE IF NOT EXISTS recommendations (
    rec_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    action TEXT NOT NULL,
    rationale TEXT NOT NULL,
    confidence REAL NOT NULL,
    expected_impact TEXT,
    status TEXT NOT NULL DEFAULT 'PROPOSED',
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS recommendation_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    implemented_at TEXT,
    observed_7d_lift REAL,
    notes TEXT,
    FOREIGN KEY(rec_id) REFERENCES recommendations(rec_id)
);

CREATE TABLE IF NOT EXISTS external_context (
    context_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    context_date TEXT NOT NULL,
    summary TEXT NOT NULL,
    tags TEXT
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    conn = connect(db_path)
    with conn:
        conn.executescript(SCHEMA)
    conn.close()
