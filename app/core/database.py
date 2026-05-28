from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


def resolved_database_url() -> str:
    raw = str(settings.DATABASE_URL or '').strip()
    if not raw.startswith('sqlite:///'):
        return raw
    sqlite_path = raw[len('sqlite:///'):]
    if sqlite_path.startswith('/'):
        return raw
    db_path = (Path(__file__).resolve().parents[2] / sqlite_path).resolve()
    return f'sqlite:///{db_path}'


engine = create_engine(
    resolved_database_url(),
    connect_args={'check_same_thread': False} if resolved_database_url().startswith('sqlite') else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
