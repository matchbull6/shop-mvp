import logging
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from miniopy_async.api import Minio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import config
from app.api import router
from app.db import create_tables
from app.storage import ImageStorage

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    engine = create_async_engine(config.DATABASE_URL, pool_pre_ping=True)
    await create_tables(engine)
    app.state.session_factory = async_sessionmaker(engine, expire_on_commit=False)

    minio = Minio(
        config.MINIO_URL,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=False,
    )
    storage = ImageStorage(minio, config.MINIO_BUCKET)
    await storage.ensure_bucket()
    app.state.storage = storage

    yield

    await minio.close_session()
    await engine.dispose()


app = FastAPI(
    title="Shop MVP",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.include_router(router)
