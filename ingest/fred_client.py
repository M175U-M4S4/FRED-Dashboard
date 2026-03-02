from __future__ import annotations

import hashlib
import os
from datetime import date
from typing import Any

import numpy as np
import pandas as pd
import requests

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


class FredClient:
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.timeout = timeout

    def fetch_observations(self, series_id: str, history_years: int | str = 20) -> tuple[pd.DataFrame, str]:
        if self.api_key:
            df = self._fetch_from_fred(series_id, history_years)
            if not df.empty:
                return df, "fred"
        return self._synthetic_series(series_id, history_years), "synthetic"

    def _fetch_from_fred(self, series_id: str, history_years: int | str) -> pd.DataFrame:
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "sort_order": "asc",
        }
        if history_years != "all":
            years = int(history_years)
            params["observation_start"] = f"{max(1900, date.today().year - years)}-01-01"
        resp = requests.get(BASE_URL, params=params, timeout=self.timeout)
        resp.raise_for_status()
        payload = resp.json()
        obs = payload.get("observations", [])
        rows: list[dict[str, Any]] = []
        for row in obs:
            value = row.get("value")
            if value in (None, "."):
                continue
            rows.append({"date": row["date"], "value": float(value)})
        return pd.DataFrame(rows)

    def _synthetic_series(self, series_id: str, history_years: int | str) -> pd.DataFrame:
        if history_years == "all":
            periods = 240
        else:
            periods = max(36, int(history_years) * 12)
        dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=periods, freq="MS")

        seed = int(hashlib.sha256(series_id.encode("utf-8")).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        trend = np.linspace(0, 25, periods)
        seasonal = 3.5 * np.sin(np.linspace(0, 18, periods))
        noise = rng.normal(0, 0.8, periods)
        base = 100 + trend + seasonal + noise

        return pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "value": base.round(4)})
