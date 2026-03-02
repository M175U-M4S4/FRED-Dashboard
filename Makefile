.PHONY: setup ingest api ui test format

PYTHON ?= python
VENV_PY ?= .venv/bin/python

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt

ingest:
	$(VENV_PY) -m ingest.run

api:
	$(VENV_PY) -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

ui:
	$(VENV_PY) -m streamlit run app/main.py --server.port 8501

test:
	$(VENV_PY) -m pytest -q
