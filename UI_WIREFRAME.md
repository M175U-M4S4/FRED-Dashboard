-- DuckDB/SQLite schema for FRED Dashboard V2
-- Keep raw vs derived separate.

CREATE TABLE IF NOT EXISTS series_catalog (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT NOT NULL,
  tier TEXT NOT NULL,
  intent TEXT,
  frequency_hint TEXT,
  history_years TEXT,
  chart TEXT,
  transforms TEXT,          -- JSON string
  notes TEXT,
  fallback_ids TEXT,        -- JSON string
  vintage BOOLEAN,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS series_metadata (
  id TEXT,
  fetched_at TIMESTAMP,
  json TEXT,                -- raw /fred/series response json
  PRIMARY KEY (id, fetched_at)
);

CREATE TABLE IF NOT EXISTS observations_raw (
  id TEXT NOT NULL,                 -- series id
  date DATE NOT NULL,
  value DOUBLE,
  realtime_start DATE,
  realtime_end DATE,
  is_latest BOOLEAN DEFAULT TRUE,   -- when vintage=true, mark latest
  fetched_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id, date, realtime_start, realtime_end)
);

CREATE TABLE IF NOT EXISTS observations_derived (
  id TEXT NOT NULL,                 -- derived id, e.g. PAYEMS__yoy
  base_id TEXT NOT NULL,            -- PAYEMS
  transform TEXT NOT NULL,          -- yoy/mom/diff/zscore/spread_to etc
  date DATE NOT NULL,
  value DOUBLE,
  fetched_at TIMESTAMP NOT NULL,
  PRIMARY KEY (id, date)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
  run_id TEXT PRIMARY KEY,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  status TEXT,                      -- success/partial/fail
  config_hash TEXT,
  summary_json TEXT                 -- counts, failures, durations
);

CREATE TABLE IF NOT EXISTS ingestion_events (
  run_id TEXT,
  id TEXT,
  level TEXT,                       -- info/warn/error
  message TEXT,
  detail_json TEXT,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
