from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    """Open the MongoDB connection required by the RAG API at startup.

    Returns:
        None: The database handle is attached to the FastAPI app so upload and
        processing routes can persist projects, assets, and chunks.
    """
    settings = get_settings()
    # Share one client across requests instead of opening a connection per call.
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongodb_conn[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close the shared MongoDB connection when the RAG API stops.

    Returns:
        None: Closing the client releases database resources cleanly.
    """
    app.mongodb_conn.close()


app.include_router(base.base_router)
app.include_router(data.data_router)

