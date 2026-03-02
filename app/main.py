from __future__ import annotations

from datetime import date

import pandas as pd
import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="FRED Dashboard V2", layout="wide")
st.title("FRED Dashboard V2")


@st.cache_data(ttl=60)
def api_get(path: str, params: dict | None = None):
    resp = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


col_top1, col_top2 = st.columns([1, 3])
with col_top1:
    if st.button("🔄 Refresh ingestion + data"):
        st.cache_data.clear()
        st.success("Cache cleared. Re-open selection to fetch latest API data.")
with col_top2:
    health = api_get("/health")
    st.caption(f"API status: **{health['status']}** | DB exists: **{health['db_exists']}** | {health['time']}")

domains = api_get("/domains")
selected_domain = st.sidebar.selectbox("Domain", domains)

series_list = api_get("/series", params={"domain": selected_domain})
if not series_list:
    st.warning("No enabled series in this domain.")
    st.stop()

series_label_map = {f"{s['id']} — {s['name']}": s["id"] for s in series_list}
selected_label = st.sidebar.selectbox("Series", list(series_label_map.keys()))
selected_series_id = series_label_map[selected_label]

payload = api_get(f"/series/{selected_series_id}", params={"limit": 2000})
meta = payload["metadata"]
obs = payload["observations"]

if not obs:
    st.warning("No observations found. Run ingestion first.")
    st.stop()

df = pd.DataFrame(obs)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

start_default = df["date"].min().date()
end_default = df["date"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Date range", value=(start_default, end_default), min_value=start_default, max_value=end_default
)

if isinstance(start_date, date) and isinstance(end_date, date):
    filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)].copy()
else:
    filtered = df.copy()

st.subheader(f"{meta['name']} ({meta['id']})")
st.caption(f"Domain: {meta['domain']} | Tier: {meta['tier']} | Frequency hint: {meta['frequency_hint']}")
st.line_chart(filtered.set_index("date")["value"])

latest = filtered.tail(1)
latest_value = float(latest["value"].iloc[0]) if not latest.empty else None
latest_date = latest["date"].dt.strftime("%Y-%m-%d").iloc[0] if not latest.empty else "N/A"

c1, c2, c3 = st.columns(3)
c1.metric("Latest Value", "N/A" if latest_value is None else f"{latest_value:,.4f}")
c2.metric("Latest Date", latest_date)
c3.metric("Rows Shown", str(len(filtered)))

st.markdown("### Latest Observations")
st.dataframe(
    filtered[["date", "value", "source", "fetched_at"]]
    .sort_values("date", ascending=False)
    .head(20)
    .reset_index(drop=True),
    use_container_width=True,
)
