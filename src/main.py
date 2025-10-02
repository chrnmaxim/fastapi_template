from fastapi import FastAPI
from fastapi.responses import HTMLResponse, ORJSONResponse

from src.api_config import api_settings
from src.healthcheck.router import healthcheck_router

app = FastAPI(
    title=api_settings.APP_NAME,
    description=f"{api_settings.APP_NAME} in {api_settings.MODE} mode.",
    version=api_settings.APP_VERSION,
    swagger_ui_parameters={
        "operationsSorter": "method",  # Sort endpoints in group in alphabetical order
        "defaultModelsExpandDepth": -1,  # Hide response schemas from docs
    },
    docs_url="/docs" if api_settings.MODE != "PROD" else None,
    redoc_url="/redoc" if api_settings.MODE != "PROD" else None,
    openapi_url="/openapi.json" if api_settings.MODE != "PROD" else None,
    default_response_class=ORJSONResponse,  # JSON response using the high-performance orjson library to serialize data to JSON
)

routers = (healthcheck_router,)
for router in routers:
    app.include_router(router=router, prefix="/api/v1")


if api_settings.MODE != "PROD":

    @app.get(path="/", response_class=HTMLResponse, include_in_schema=False)
    def home() -> str:
        return f"""
        <html>
        <head><title>{app.title}</title></head>
        <body>
        <h1>{app.description}</h1>
        <ul>
        <li><a href="/docs">Swagger</a></li>
        <li><a href="/redoc">ReDoc</a></li>
        </ul>
        </body>
        </html>
        """
