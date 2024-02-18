from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    
    SQL_DB_URI: PostgresDsn