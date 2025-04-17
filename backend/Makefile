.PHONY: run test lint format clean migrate-up migrate-down migrate-revision seed install dev help

# Default Python interpreter
PYTHON = python

# Poetry command
POETRY = poetry

# Default port for the server
PORT = 8000

# Default host for the server
HOST = 0.0.0.0

# Default reload flag
RELOAD = --reload

help:
	@echo "Available commands:"
	@echo "  make run              - Run the FastAPI server with reload"
	@echo "  make run-prod         - Run the FastAPI server in production mode (no reload)"
	@echo "  make test             - Run tests"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make lint             - Run linting (flake8)"
	@echo "  make format           - Format code with black"
	@echo "  make clean            - Remove Python cache files"
	@echo "  make migrate-revision - Create a new migration revision (requires message)"
	@echo "  make migrate-up       - Run migrations up"
	@echo "  make migrate-down     - Roll back migrations"
	@echo "  make seed             - Seed the database with initial data"
	@echo "  make install          - Install dependencies"
	@echo "  make dev              - Install dev dependencies"

run:
	$(POETRY) run fastapi dev

run-prod:
	$(POETRY) run uvicorn main:app --host $(HOST) --port $(PORT)

test:
	$(POETRY) run pytest

test-cov:
	$(POETRY) run pytest --cov=. --cov-report=term-missing

lint:
	$(POETRY) run flake8 .

format:
	$(POETRY) run black .

clean:
	powershell -Command "Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force"
	powershell -Command "Get-ChildItem -Path . -Include *.pyc,*.pyo,*.pyd,.coverage -Recurse -File | Remove-Item -Force"
	powershell -Command "Get-ChildItem -Path . -Include *.egg-info,*.egg,.pytest_cache,.coverage,htmlcov,.mypy_cache -Recurse -Directory | Remove-Item -Recurse -Force"

migrate-revision:
	$(POETRY) run alembic revision --autogenerate -m $(message)
# Usage: make migrate-revision message="your migration message"

migrate-up:
	$(POETRY) run alembic upgrade head

migrate-down:
	$(POETRY) run alembic downgrade -1

seed:
	$(POETRY) run python seed.py

install:
	$(POETRY) install --no-dev

dev:
	$(POETRY) install
