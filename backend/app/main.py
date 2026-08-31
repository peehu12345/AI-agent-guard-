"""
AgentGuard — AI Control Tower for Autonomous Payment & Revenue Agents
FastAPI main application entry point.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.api import analytics, simulation, decisions, conflicts, reviews, agents, policies

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("agentguard")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables. Shutdown: cleanup."""
    logger.info("AgentGuard starting up — creating database tables...")
    await create_tables()
    logger.info("Database ready.")
    yield
    logger.info("AgentGuard shutting down.")


app = FastAPI(
    title="AgentGuard — AI Control Tower",
    description="Governance and supervisory layer for autonomous payment & revenue agents",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(analytics.router)
app.include_router(simulation.router)
app.include_router(decisions.router)
app.include_router(conflicts.router)
app.include_router(reviews.router)
app.include_router(agents.router)
app.include_router(policies.router)


@app.get("/")
async def root():
    return {
        "name": "AgentGuard",
        "tagline": "AI Control Tower for Autonomous Payment & Revenue Agents",
        "status": "operational",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
