from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(env_file="./.env",
                                  env_ignore_empty=True,
                                  extra="ignore")

class DatabaseSettings(BaseSettings):
    model_config = _base_config
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    @property
    def db_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")