# RUN THIS ONCE TO CREATE THE DATABASE
from sqlmodel import SQLModel
from app.db.models.user import User
from app.db.session import engine

SQLModel.metadata.create_all(engine)
