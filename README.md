# FRED Dashboard V2

FRED Dashboard V2 is a local, Windows-friendly macro dashboard with:
- **Ingestion** (FRED API or deterministic synthetic fallback)
- **FastAPI** backend
- **Streamlit** frontend
- **Dataset catalog driven by** `config/DATASETS_V2.yaml` (single source of truth)

> No local DB files are committed. The runtime database is created under `data/`.

---

## Quick Start (Windows, no command line needed)

1. **Double-click `01_setup_once.bat`**
   - Creates `.venv`
   - Installs dependencies from `requirements.txt`

2. **(Optional) Set API key**
   - Create a file named `.env` in the project root.
   - Add:
     ```
     FRED_API_KEY=your_fred_api_key_here
     ```
   - If missing, synthetic data is generated so the app still runs.

3. **Double-click `02_run_dashboard.bat`**
   - Runs ingestion
   - Starts API at `http://127.0.0.1:8000`
   - Starts UI at `http://127.0.0.1:8501`
   - Opens browser automatically

---

## API Endpoints

- `GET /health`
- `GET /domains`
- `GET /series?domain=<domain_name>`
- `GET /series/{series_id}?limit=200`
- `GET /composites`

---

## Catalog-Driven Design

All domains, series, and composites are defined in:

- `config/DATASETS_V2.yaml`

No ingestion/API/UI logic should hardcode FRED series IDs.

---

## Development (optional)

If you prefer terminal-based workflows:

- `make setup`
- `make ingest`
- `make api`
- `make ui`
- `make test`

---

## Troubleshooting (Windows)

- **`py` not found**
  - Install Python 3.10+ from python.org and enable “Add Python to PATH”.

- **Port already in use (8000 or 8501)**
  - Close old Python windows from Task Manager and rerun `02_run_dashboard.bat`.

- **Blank dashboard or no data**
  - Rerun `02_run_dashboard.bat` to re-ingest.
  - Check `.env` for valid `FRED_API_KEY`.
  - Without API key, synthetic data should still appear.

- **Dependency install fails**
  - Re-run `01_setup_once.bat`.
  - Check internet/proxy settings.

---

## Repo Layout (target)

```
.
├─ app/main.py
├─ api/main.py
├─ ingest/
│  ├─ run.py
│  ├─ fred_client.py
│  ├─ db.py
│  ├─ config.py
│  └─ transforms.py
├─ config/DATASETS_V2.yaml
├─ data/.gitkeep
├─ tests/
│  ├─ test_catalog.py
│  └─ test_transforms.py
├─ requirements.txt
├─ Makefile
├─ .gitignore
├─ README.md
├─ 01_setup_once.bat
└─ 02_run_dashboard.bat
```
