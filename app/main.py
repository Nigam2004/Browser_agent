from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router
from app.core.config import settings
from app.services.browser_sessions import close_all_sessions


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await close_all_sessions()


app = FastAPI(
    title="Mantra Browser Automation Agent",
    version="0.1.0",
    lifespan=lifespan,
)

settings.screenshots_dir.mkdir(parents=True, exist_ok=True)
app.mount(
    "/screenshots",
    StaticFiles(directory=str(settings.screenshots_dir)),
    name="screenshots",
)
app.include_router(router)
