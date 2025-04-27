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
    allow_origins=["*"],    # Allow all origins for testing
    allow_credentials=False,  # Changed to False because wildcard origin requires this
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Root route for testing
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Divine AI API is running"}

# Add a middleware to handle OPTIONS requests
@app.middleware("http")
async def options_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return JSONResponse(
            content={"message": "CORS preflight handled"},
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Max-Age": "86400",  # Cache preflight for 24 hours
            },
        )
    return await call_next(request)

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
