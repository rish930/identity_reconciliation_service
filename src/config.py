from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from typing import Optional
import os

from dotenv import load_dotenv


class Settings(BaseSettings):
    
    SQL_DB_URI: Optional[PostgresDsn] = None
    SQL_ENGINE_ECHO: bool = False


class TestSettings(Settings):

    SQL_DB_URI: Optional[PostgresDsn] = "postgresql://bitespeed_test:bitespeedtest@localhost/fluxkart_customer_test_db"
    SQL_ENGINE_ECHO: bool = True


def get_settings():
    if os.getenv('APP_ENV', 'prod')=='prod':
        load_dotenv()
        return Settings()
    else:
        return TestSettings()
    

settings = get_settings()