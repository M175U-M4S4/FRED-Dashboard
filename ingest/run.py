from __future__ import annotations

import json
from datetime import datetime

from ingest.config import AppConfig, load_catalog
from ingest.db import connect, init_db, upsert_observations, upsert_series_catalog
from ingest.fred_client import FredClient


def run_ingestion() -> dict:
    cfg = AppConfig()
    catalog = load_catalog(cfg.catalog_path)

    conn = connect(cfg.db_path)
    init_db(conn)

    series_rows = []
    for s in catalog["series"]:
        series_rows.append(
            {
                "series_id": s["id"],
                "name": s["name"],
                "domain": s["domain"],
                "tier": s["tier"],
                "enabled": 1 if s["enabled"] else 0,
                "frequency_hint": s["frequency_hint"],
                "history_years": str(s["history_years"]),
                "transforms_json": json.dumps(s["transforms"]),
                "chart": s["chart"],
                "notes": s["notes"],
                "fallback_ids_json": json.dumps(s["fallback_ids"]),
                "vintage": 1 if s["vintage"] else 0,
                "intent": s["intent"],
            }
        )
    upsert_series_catalog(conn, series_rows)

    client = FredClient()
    ingested_rows = 0
    per_series = []

    for s in catalog["series"]:
        if not s["enabled"]:
            continue

        df, source = client.fetch_observations(s["id"], s["history_years"])
        rows = [
            {
                "series_id": s["id"],
                "date": str(r["date"]),
                "value": float(r["value"]),
                "source": source,
            }
            for r in df.to_dict(orient="records")
        ]
        ingested_rows += upsert_observations(conn, rows)
        per_series.append({"series_id": s["id"], "rows": len(rows), "source": source})

    conn.close()
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "db_path": str(cfg.db_path),
        "series_processed": len(per_series),
        "rows_upserted": ingested_rows,
        "details": per_series,
    }


if __name__ == "__main__":
    summary = run_ingestion()
    print(json.dumps(summary, indent=2))
