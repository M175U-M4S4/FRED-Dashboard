FRED Dashboard V2 — Backend API Contract (FastAPI)

Base URL
- /api

Endpoints
1) GET /api/domains
Response: [{ "domain": "Liquidity", "count": 4 }, ...]

2) GET /api/series
Query params:
- domain (optional)
- tier (optional)
Response: [{ id, name, domain, tier, intent, chart, transforms, notes }, ...]

3) GET /api/series/{id}
Returns catalog entry + latest metadata snapshot

4) GET /api/series/{id}/data
Query params:
- start=YYYY-MM-DD (optional)
- end=YYYY-MM-DD (optional)
- transform=lin|yoy|mom|diff|zscore|...
- vintage=latest|all (default latest)
Response:
{
  "id": "PAYEMS",
  "transform": "yoy",
  "observations": [{ "date": "2024-01-01", "value": 1.23 }, ...]
}

5) GET /api/composites
Response: [{ id, name, intent, chart }, ...]

6) GET /api/composites/{id}/data
Response depends on chart:
- line_zero: { date,value } series
- multi_panel: { panels: { key: [{date,value}...] } }
- heatmap_band: { score: [{date,value}], bands: {...} }

7) GET /api/health
Response: { status, last_successful_run, failed_series_count, version }

Notes
- All responses are JSON.
- CORS enabled for local UI.
- Authentication optional (basic auth behind reverse proxy is fine).
