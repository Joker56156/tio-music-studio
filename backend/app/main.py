from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import generation, tracks, audio, system


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title="TIO Music Studio",
    description="Local AI music generation API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation.router, prefix="/api", tags=["generation"])
app.include_router(tracks.router, prefix="/api", tags=["tracks"])
app.include_router(audio.router, prefix="/api", tags=["audio"])
app.include_router(system.router, prefix="/api", tags=["system"])
