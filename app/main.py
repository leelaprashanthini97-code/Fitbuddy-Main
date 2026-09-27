from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router


app = FastAPI(
    title="FitBuddy AI",
    description="AI Wellness Plan Generator",
    version="1.0"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(router)
