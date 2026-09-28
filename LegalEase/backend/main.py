from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from config import settings


app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document generator",
    version="1.0.0"
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "name": "LegalEase API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }