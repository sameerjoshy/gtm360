from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="GTM360 Revenue OS",
    version="1.0.0",
    description="Unified agent backend: researcher, hygiene, sales, content, briefing, outbound.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "service": "gtm360-api",
        "environment": settings.environment,
        "docs": "/docs",
    }