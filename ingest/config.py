from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT_DIR / "config" / "DATASETS_V2.yaml"
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "fred_dashboard_v2.sqlite"


@dataclass
class AppConfig:
    catalog_path: Path = CATALOG_PATH
    db_path: Path = DB_PATH


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    catalog_path = path or CATALOG_PATH
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog file not found: {catalog_path}")

    raw = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    series = _as_list(raw.get("series"))
    composites = _as_list(raw.get("composites"))

    normalized_series: list[dict[str, Any]] = []
    for item in series:
        if not isinstance(item, dict):
            continue
        entry = {
            "id": str(item.get("id", "")).strip(),
            "name": str(item.get("name", "")).strip(),
            "domain": str(item.get("domain", "General")).strip() or "General",
            "tier": str(item.get("tier", "B")).strip() or "B",
            "enabled": bool(item.get("enabled", True)),
            "frequency_hint": str(item.get("frequency_hint", "monthly")).strip() or "monthly",
            "history_years": item.get("history_years", 20),
            "transforms": _as_list(item.get("transforms")),
            "chart": str(item.get("chart", "line")).strip() or "line",
            "notes": str(item.get("notes", "")).strip(),
            "fallback_ids": _as_list(item.get("fallback_ids")),
            "vintage": bool(item.get("vintage", False)),
            "intent": str(item.get("intent", "")).strip(),
        }
        if entry["id"]:
            normalized_series.append(entry)

    normalized_composites: list[dict[str, Any]] = []
    for item in composites:
        if not isinstance(item, dict):
            continue
        cid = str(item.get("id", "")).strip()
        if not cid:
            continue
        normalized_composites.append(
            {
                "id": cid,
                "name": str(item.get("name", cid)).strip() or cid,
                "description": str(item.get("description", "")).strip(),
                "domain": str(item.get("domain", "Composites")).strip() or "Composites",
                "components": _as_list(item.get("components")),
                "method": str(item.get("method", "mean")).strip() or "mean",
                "enabled": bool(item.get("enabled", True)),
            }
        )

    return {"series": normalized_series, "composites": normalized_composites}
