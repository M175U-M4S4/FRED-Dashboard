FRED Dashboard V2

Quickstart
1) Create FRED API key and set config/.env (see config/.env.example)
2) make setup
3) make ingest
4) make run-api   (http://127.0.0.1:8000)
5) make run-ui    (http://127.0.0.1:8501)

Design Principles
- Catalog-driven indicators (config/DATASETS_V2.yaml)
- Raw vs derived separation
- Resilient ingestion (retry + rate limit + caching + fallback_ids)
- Composite analytics as first-class outputs

See:
- SPEC_V2.md
- API_SPEC.md
- DB_SCHEMA.sql
- UI_WIREFRAME.md
- ACCEPTANCE_CRITERIA.md
