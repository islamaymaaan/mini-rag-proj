from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings,Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    """Return basic application information for an API health-style response.

    Args:
        app_settings (Settings): Dependency-injected application configuration.

    Returns:
        dict[str, str]: API name and version. This route does not process RAG
        data, but confirms the service hosting the pipeline is available.
    """
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
