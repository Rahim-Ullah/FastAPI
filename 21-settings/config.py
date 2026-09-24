from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Default App Name"
    admin_email: str = "default@example.com"
    secret_key: str = "default_secret"
    database_name: str = "simple.db"

    # Automatically load values from the .env file
    model_config = SettingsConfigDict(env_file=".env")


# Create a single settings instance to use across the project
settings = Settings()
