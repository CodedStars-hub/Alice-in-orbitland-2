PYTHON := .venv/bin/python
.PHONY: install api web lint typecheck test build check
install:
	python3.12 -m venv .venv
	$(PYTHON) -m pip install -r requirements-dev.lock
	$(PYTHON) -m pip install --no-build-isolation --no-deps -e packages/lunar_core -e apps/api
	npm ci
api:
	$(PYTHON) -m uvicorn lunar_api.app:create_app --factory --reload --host 127.0.0.1
web:
	npm run dev
lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
	npm run lint
typecheck:
	$(PYTHON) -m mypy
	npm run typecheck
test:
	$(PYTHON) -m pytest
	npm test
build:
	npm run build
check: lint typecheck test build
