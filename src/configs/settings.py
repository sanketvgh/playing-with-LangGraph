from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    langsmith_tracing: str = Field(alias="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field(alias="LANGSMITH_ENDPOINT")
    langsmith_api_key: str = Field(alias="LANGSMITH_API_KEY")
    langsmith_project_name: str = Field(alias="LANGSMITH_PROJECT")
    mistral_api_key: str = Field(alias="MISTRAL_API_KEY")

    model_config = SettingsConfigDict(
        extra="ignore", env_file="../.env", env_file_encoding="utf-8")


settings = Settings()
