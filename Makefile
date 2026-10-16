.PHONY: help install dev dev-backend dev-frontend test lint clean

help:
	@echo "ClaimGuard AI Development Commands:"
	@echo "  make install       - Install both backend and frontend dependencies"
	@echo "  make dev           - Run backend & Next.js frontend concurrently (Access via single port: 3000)"
	@echo "  make dev-backend   - Start FastAPI development server (port 8080)"
	@echo "  make dev-frontend  - Start Next.js frontend server (port 3000, proxies /api to 8080)"
	@echo "  make test          - Run backend unit and integration tests"
	@echo "  make lint          - Run Ruff linter on backend"
	@echo "  make clean         - Clean cache and build artifacts"

install:
	cd backend && python3 -m pip install -r requirements.txt
	cd frontend && npm install

dev:
	@echo "Starting ClaimGuard AI on http://localhost:3000 (Backend proxied automatically)..."
	make -j 2 dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8080

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -v

lint:
	cd backend && ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf frontend/.next
