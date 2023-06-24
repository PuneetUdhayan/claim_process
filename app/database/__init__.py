import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_DB = quote_plus(os.environ["POSTGRES_DB"])
POSTGRES_HOST = quote_plus(os.environ["POSTGRES_HOST"])
POSTGRES_USER = quote_plus(os.environ["POSTGRES_USER"])
POSTGRES_PASSWORD = quote_plus(os.environ["POSTGRES_PASSWORD"])

SQLALCHAMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
