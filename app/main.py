from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.routes import ask, auth, user
from app.db.init_db import create_db_and_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS - use wildcard to allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://localhost:8080",
        "http://127.0.0.1:8080",  # Add alternative localhost
        "https://divine-ai.vercel.app",
        "http://divine-ai.vercel.app",
    ],
    allow_credentials=True,  # Enable credentials
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Root route for testing
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Divine AI API is running"}

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(ask.router)

@app.on_event("startup")
async def on_startup():
    """Run tasks at application startup"""
    logger.info("Application starting up...")
    # Create database tables
    create_db_and_tables()
    logger.info("Application startup completed")
