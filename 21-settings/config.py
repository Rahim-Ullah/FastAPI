from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory for the settings project
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str = "Default App Name"
    admin_email: str = "default@example.com"
    secret_key: str = "default_secret"
    database_name: str = "simple.db"

    # Automatically load values from the .env file located in this directory
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_path(self) -> Path:
        """Return the absolute path to the database file within the project directory."""
        return BASE_DIR / self.database_name


# Create a single settings instance to use across the project
settings = Settings()
