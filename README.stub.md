.PHONY: setup ingest run-api run-ui test lint format

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

ingest:
	. .venv/bin/activate && python -m ingest.run --config config/DATASETS_V2.yaml --env config/.env

run-api:
	. .venv/bin/activate && uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

run-ui:
	. .venv/bin/activate && streamlit run app/main.py

test:
	. .venv/bin/activate && pytest -q
