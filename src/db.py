from src.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DB_URI = settings.SQL_DB_URI.unicode_string()

engine = create_engine(SQLALCHEMY_DB_URI, echo=settings.SQL_ENGINE_ECHO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
