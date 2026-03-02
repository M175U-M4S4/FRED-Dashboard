from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS series_catalog (
            series_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            tier TEXT,
            enabled INTEGER NOT NULL DEFAULT 1,
            frequency_hint TEXT,
            history_years TEXT,
            transforms_json TEXT,
            chart TEXT,
            notes TEXT,
            fallback_ids_json TEXT,
            vintage INTEGER NOT NULL DEFAULT 0,
            intent TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS observations (
            series_id TEXT NOT NULL,
            date TEXT NOT NULL,
            value REAL,
            fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            source TEXT NOT NULL,
            PRIMARY KEY (series_id, date)
        );

        CREATE INDEX IF NOT EXISTS idx_observations_series_date
          ON observations(series_id, date);
        """
    )
    conn.commit()


def upsert_series_catalog(conn: sqlite3.Connection, rows: list[dict[str, Any]]) -> None:
    sql = """
    INSERT INTO series_catalog (
        series_id, name, domain, tier, enabled, frequency_hint,
        history_years, transforms_json, chart, notes,
        fallback_ids_json, vintage, intent, updated_at
    ) VALUES (
        :series_id, :name, :domain, :tier, :enabled, :frequency_hint,
        :history_years, :transforms_json, :chart, :notes,
        :fallback_ids_json, :vintage, :intent, CURRENT_TIMESTAMP
    )
    ON CONFLICT(series_id) DO UPDATE SET
        name=excluded.name,
        domain=excluded.domain,
        tier=excluded.tier,
        enabled=excluded.enabled,
        frequency_hint=excluded.frequency_hint,
        history_years=excluded.history_years,
        transforms_json=excluded.transforms_json,
        chart=excluded.chart,
        notes=excluded.notes,
        fallback_ids_json=excluded.fallback_ids_json,
        vintage=excluded.vintage,
        intent=excluded.intent,
        updated_at=CURRENT_TIMESTAMP;
    """
    conn.executemany(sql, rows)
    conn.commit()


def upsert_observations(conn: sqlite3.Connection, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    sql = """
    INSERT INTO observations (series_id, date, value, source)
    VALUES (:series_id, :date, :value, :source)
    ON CONFLICT(series_id, date) DO UPDATE SET
      value=excluded.value,
      source=excluded.source,
      fetched_at=CURRENT_TIMESTAMP;
    """
    conn.executemany(sql, rows)
    conn.commit()
    return len(rows)
