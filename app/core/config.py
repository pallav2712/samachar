from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    currents_api_key: str
    gemini_api_key: str
    groq_api_key: str
    openrouter_api_key: str
    telegram_bot_token: str
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()