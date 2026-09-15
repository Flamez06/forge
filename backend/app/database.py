from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://forge:forge@forge-postgres:5432/forge"
)

engine = create_engine(DATABASE_URL)
# Create a session factory that will be used to create new database sessions. 
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
# Yield is used to pause the function and return a value, while finally ensures that the database session is closed after the request is completed.
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
    
Base = declarative_base()