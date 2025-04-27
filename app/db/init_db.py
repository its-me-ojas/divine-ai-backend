from sqlmodel import SQLModel
import logging
from .session import engine

# Import all models to ensure they're registered with SQLModel
from .models.user import User
# Import any other models here

logger = logging.getLogger(__name__)

def create_db_and_tables():
    """
    Create database tables if they don't exist.
    This function should be called at application startup.
    """
    logger.info("Creating database tables if they don't exist...")
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

if __name__=="__main__":
    create_db_and_tables()
