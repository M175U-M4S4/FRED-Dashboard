FRED Dashboard V2 — Product & Technical Specification (for Codex)

Goal
- Build a private, self-hosted macro dashboard that focuses on FRED’s unique value: authoritative source, consistent metadata, stable series IDs, and multi-series/composite analytics.
- Produce a robust ingestion + storage + API + UI stack that survives intermittent API errors, rate limits, and series quirks.
- V2 must be "indicator-catalog driven": adding a series should require only editing DATASETS_V2.yaml (no code edits).

Non-goals
- Not a generic “chart everything” macro site.
- Not a public multi-tenant service.
- No brokerage execution / trading automation.

Users & Use-cases
- Single user (private access)
- Daily macro check: liquidity, stress, credit, curve, labor, inflation
- Event-driven drilldown: “why did rates move?” “is credit tightening?” “is labor cooling?”
- Composite views: recession risk, inflation drivers, risk-on/off regime

System Overview
1) Ingestion Service (Python)
- Reads indicator catalog (DATASETS_V2.yaml)
- Pulls observations via FRED API: /fred/series/observations
- Supports: frequency aggregation, units transforms (e.g., yoy, mom), vintage support (ALFRED-style via realtime_start/realtime_end)
- Rate limiting + retries + caching
- Writes normalized data to DB

2) Storage (DuckDB recommended, SQLite acceptable)
- Stores raw observations (date, value, realtime_start/end) + metadata snapshots
- Stores derived series (computed transforms) as separate table or view
- Stores ingestion logs & health metrics

3) Backend API (FastAPI)
- Read-only JSON endpoints for UI
- Endpoints: list domains, list series, fetch series data, fetch composites, health

4) Frontend (Web)
Option A (fast): Streamlit app with dark theme + tabs per domain + composite dashboards
Option B (flex): Vite + React + lightweight charts (uPlot / echarts) consuming FastAPI

Key V2 Improvements over V1
- “No deletions because of API hiccups”: implement fallback series & graceful degradation.
- Strong correctness checks: verify series exists; detect “.” missing values; enforce monotonic date ordering; store last_successful sync.
- Composite analytics are first-class: defined in catalog and computed server-side.
- Clear separation: raw vs derived data; domain views vs composite views.

Data Policy
- Default history: 20 years (configurable per series), but allow “full history” for slow-moving structural series (e.g., WALCL).
- Update cadence per series frequency:
  - Daily: 1–6 hours
  - Weekly: daily
  - Monthly: daily
  - Quarterly: weekly
- Retain all revisions (vintages) for series marked vintage=true; otherwise store latest only.

Reliability Requirements
- Global rate limit: configurable (default 60 req/min to be safe; allow 120 req/min if verified)
- Automatic retries with exponential backoff for 429/5xx/timeouts
- Cache GET responses for 24h (etag not available) and for backfills (disk cache)
- Backup rotation: keep N daily DB snapshots (e.g., 14)

Security
- Local-only by default
- Optional basic auth + reverse proxy (Caddy/Nginx) for remote private access
- FRED API key in .env only

Deliverables
- Repo scaffold + runnable with: `make setup && make ingest && make run`
- Indicator catalog (DATASETS_V2.yaml) covering “Complete Domains” + “Composite Analyses”
- Tests for: catalog validation, ingestion correctness, transform correctness
