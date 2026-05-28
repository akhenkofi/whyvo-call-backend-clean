from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str = 'Whyvo Call API'
    SECRET_KEY: str = 'change-me'
    DATABASE_URL: str = 'sqlite:///./whyvo_call.db'
    FRONTEND_ORIGINS: str = 'http://127.0.0.1:5173'
    WHYVO_AGORA_APP_ID: str = ''
    WHYVO_AGORA_APP_CERTIFICATE: str = ''


settings = Settings()
