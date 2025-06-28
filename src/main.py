from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth.router import router as auth_router
from .common.db import create_db_and_tables
from .post.router import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(post_router)
