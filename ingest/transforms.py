from __future__ import annotations

import pandas as pd


def compute_yoy(series: pd.Series) -> pd.Series:
    return series.pct_change(12) * 100.0


def compute_mom(series: pd.Series) -> pd.Series:
    return series.pct_change(1) * 100.0


def compute_diff(series: pd.Series) -> pd.Series:
    return series.diff(1)


def compute_zscore(series: pd.Series, window: int = 52) -> pd.Series:
    rolling_mean = series.rolling(window=window, min_periods=max(8, window // 4)).mean()
    rolling_std = series.rolling(window=window, min_periods=max(8, window // 4)).std(ddof=0)
    return (series - rolling_mean) / rolling_std
