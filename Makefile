ruff_fix:
	uv run ruff format . && uv run ruff check --fix . && uv run ruff check --fix --select I .
ruff_check:
	uv run ruff check . && uv run ruff check --select I . && uv run ruff format --check .
mypy_check:
	uv run mypy .
start_dev:
	docker compose --profile dev up -d --build
	docker container exec app-dev alembic upgrade heads
stop_dev:
	docker compose --profile dev down
remove_dev:
	docker compose --profile dev down -v
test:
	docker compose run --rm app-test
	docker compose --profile test down
start_local_db:
	docker compose up -d postgres-dev
stop_local_db:
	docker compose down postgres-dev
remove_local_db:
	docker compose down -v postgres-dev
autogenerate:
	uv run alembic revision --autogenerate -m "$(m)"
migrate:
	uv run alembic upgrade heads