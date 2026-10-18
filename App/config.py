from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    #DB
    db_url:str
    #Server 
    port:int
    #App
    version:str
    secret_key:str
    algorithm:str
    token_expires:int

settings = Settings()