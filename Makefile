.PHONY: help install test run docker-up docker-down demo lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install fastapi uvicorn[standard] pydantic httpx pytest

run: ## Start the API server locally
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run the test suite
	pytest tests/ -v

demo: ## Run the interactive demo
	python3 demo.py

docker-up: ## Start via Docker Compose
	docker-compose up --build -d

docker-down: ## Stop Docker Compose
	docker-compose down

lint: ## Run Python linter (if ruff is installed)
	ruff check src/ tests/ || echo "Install ruff: pip install ruff"

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null
	rm -rf *.egg-info build dist 2>/dev/null
	@echo "Cleaned ✓"
