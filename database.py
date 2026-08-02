from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("CRITICAL CONFIG ERROR: 'DATABASE_URL' is missing from your .env file!")


engine = create_engine(database_url, echo=False, future=True)

session = sessionmaker(bind= engine, autocommit = False, autoflush=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally: 
        db.close

