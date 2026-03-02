from __future__ import annotations

import json
import sqlite3
from datetime import datetime

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from ingest.config import AppConfig, load_catalog
from ingest.transforms import compute_diff, compute_mom, compute_yoy, compute_zscore

app = FastAPI(title="FRED Dashboard V2 API", version="2.0.0")


def get_conn() -> sqlite3.Connection:
    cfg = AppConfig()
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/health")
def health() -> dict:
    cfg = AppConfig()
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
        "db_exists": cfg.db_path.exists(),
        "catalog": str(cfg.catalog_path),
    }


@app.get("/domains")
def domains() -> list[str]:
    catalog = load_catalog()
    return sorted({s["domain"] for s in catalog["series"] if s["enabled"]})


@app.get("/series")
def list_series(domain: str | None = Query(default=None)) -> list[dict]:
    catalog = load_catalog()
    rows = [s for s in catalog["series"] if s["enabled"]]
    if domain:
        rows = [s for s in rows if s["domain"].lower() == domain.lower()]
    return rows


@app.get("/series/{series_id}")
def get_series(series_id: str, limit: int = Query(default=200, ge=1, le=5000)) -> dict:
    catalog = load_catalog()
    meta = next((s for s in catalog["series"] if s["id"].lower() == series_id.lower()), None)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Unknown series: {series_id}")

    conn = get_conn()
    try:
        cur = conn.execute(
            """
            SELECT series_id, date, value, source, fetched_at
            FROM observations
            WHERE series_id = ?
            ORDER BY date DESC
            LIMIT ?
            """,
            (meta["id"], limit),
        )
        obs = [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

    obs.reverse()
    return {"metadata": meta, "observations": obs}


@app.get("/composites")
def composites() -> list[dict]:
    catalog = load_catalog()
    enabled = [c for c in catalog["composites"] if c["enabled"]]
    conn = get_conn()
    out: list[dict] = []

    try:
        for comp in enabled:
            comp_df: pd.DataFrame | None = None
            for component in comp["components"]:
                sid = component.get("series_id")
                transform = component.get("transform", "lin")
                weight = float(component.get("weight", 1.0))
                if not sid:
                    continue

                df = pd.read_sql_query(
                    "SELECT date, value FROM observations WHERE series_id = ? ORDER BY date",
                    conn,
                    params=(sid,),
                )
                if df.empty:
                    continue
                s = pd.Series(df["value"].values, index=pd.to_datetime(df["date"]))
                if transform == "yoy":
                    s = compute_yoy(s)
                elif transform == "mom":
                    s = compute_mom(s)
                elif transform == "diff":
                    s = compute_diff(s)
                elif transform == "zscore":
                    s = compute_zscore(s)

                comp_piece = pd.DataFrame({sid: s * weight})
                comp_df = comp_piece if comp_df is None else comp_df.join(comp_piece, how="outer")

            if comp_df is None or comp_df.empty:
                out.append({"id": comp["id"], "name": comp["name"], "description": comp["description"], "observations": []})
                continue

            method = comp.get("method", "mean")
            if method == "sum":
                agg = comp_df.sum(axis=1, skipna=True)
            else:
                agg = comp_df.mean(axis=1, skipna=True)

            points = [
                {"date": idx.strftime("%Y-%m-%d"), "value": None if pd.isna(v) else float(v)}
                for idx, v in agg.dropna().items()
            ]
            out.append(
                {
                    "id": comp["id"],
                    "name": comp["name"],
                    "description": comp["description"],
                    "method": method,
                    "observations": points,
                }
            )
    finally:
        conn.close()

    return out
