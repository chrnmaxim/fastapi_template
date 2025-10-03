# FastAPI Template

[![Static Badge](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Static Badge](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Static Badge](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io)
[![Static Badge](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Static Badge](https://img.shields.io/badge/-SQLAlchemy-ffd54?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Static Badge](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

### This is a template repository to quickly start a new FastAPI project.

## Key features:
* Configured SwaggerUI, doc URLs and homepage in `src.main.app` (fastapi.FastAPI instance).
* Configured SQLAlchemy Session and Engine with [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool) as `poolclass`, `echo` mode and `application_name` for proper monitoring connections from the app to a database or a connection pooler.
* Configured [pytest](https://docs.pytest.org/en/stable/) for integration tests in Docker with independent PostgreSQL database.
* Configured [alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations.
* `BaseRepository` class as the main interface for basic CRUD operations with DB models.
* `Docker` files for tests and local app start.
* `Nginx` configuration includes optimized timeouts, connection limits.
* `Makefile` with commands for convenient usage.
* CI workflow in GitHub Actions that starts with each commit into open PR into `develop` or `main` branches.

## Optimization key points

### SQLAlchemy
* SQLAlchemy Connection Pooling with [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool) allows maintaining a connection to the database.
> [!NOTE]
> `POOL_SIZE` and `MAX_OVERFLOW` environment variables should be set taking `uvicorn --workers N` into account.
* `src.dependencies.get_session` provides an AsyncGenerator of an [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) instance with a transaction that will be automatically committed or rolled back in case of any exception upon exiting the context manager.
> [!NOTE]
> The DB connection is checked out from the pool at the first `AsyncSession.execute` call and remains so until exiting the context manager.

### FastAPI
* [ORJSONResponse](https://fastapi.tiangolo.com/advanced/custom-response/#orjsonresponse) as
`default_response_class` in FastAPI configuration which uses the high-performance [orjson](https://github.com/ijl/orjson) library to serialize data to JSON.
* [Middlewares](https://fastapi.tiangolo.com/tutorial/middleware/) are disabled, since usually the app runs behind a reverse proxy.
* [src.healthcheck.router.healthcheck](src/healthcheck/router.py) returns [ORJSONResponse](https://fastapi.tiangolo.com/advanced/custom-response/#orjsonresponse)
directly instead of the pydantic model [src.healthcheck.schemas.HealthCheckSchema](src/healthcheck/schemas.py) to avoid overcomplicated (_in some cases_) validation and serialization to an object compatible with JSON by [jsonable_encoder](https://fastapi.tiangolo.com/tutorial/encoder/).

### Uvicorn
When running uvicorn in a production/stage environment behind a reverse proxy, the startup command is:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers $UVICORN_WORKERS --loop uvloop --proxy-headers --no-access-log
```
* `--workers $UVICORN_WORKERS` - Set the number of workers according to the number of vCPUs on the server (as a startup option).
* `--loop uvloop` - Set the event loop implementation to [uvloop](https://github.com/MagicStack/uvloop) explicitly (uvloop makes asyncio 2-4x faster).
* `--proxy-headers` - Enable proxy headers.
* `--no-access-log` - Disable uvicorn access log.

> [!NOTE]
> If uvicorn and a reverse proxy are running on the same server, it is more beneficial to establish a connection via a UNIX domain socket using the `--uds <path>` option (see `docker-compose-prod.yml` and `nginx/nginx.conf` for examples).

## Use as Template

1. Create a repository from this template by clicking the [**Use this template**] button.

> [!NOTE]
> For more information about creating a repository from a template, refer to the [GitHub docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

2. Clone the created repository.

3. Navigate to the root directory of the template.

4. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

5. Install dependencies, including dependencies from the dev group.
```bash
uv sync --extra dev
```

5. Create `.env` based on `.env.example`:

```bash
cp -r src/.env.example src/.env`
```

6. Start App with PostgreSQL in Docker containers and apply [alembic](https://alembic.sqlalchemy.org/en/latest/) migrations:
```bash
make start_dev
```

7. API docs:
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

8. Stop and delete containers:
```bash
make stop_dev
```

9. Delete containers including volumes:
```bash
make remove_dev
```

## About Tests
The template has already configured [pytest](https://docs.pytest.org/en/stable/) with necessary fixtures for integration testing of endpoints in Docker with an independent PostgreSQL database. See example in `tests/integration/healthcheck_router_test.py`.

At the start of the test session, [alembic](https://alembic.sqlalchemy.org/en/latest/) migrations are applied to the database.

1. The tests are run from an independent PostgreSQL database using the command `make test`.

2. After running the tests, you can view the code coverage report in the `htmlcov/index.html` file.

> [!NOTE]
> Tests are run in GitHub Actions with each commit to an open Pull Request in the `develop` or `main` branch.
