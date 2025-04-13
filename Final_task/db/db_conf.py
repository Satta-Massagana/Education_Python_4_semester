from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Type, Generator

# Подключение к PostgreSQL
# DATABASE_URL = "postgresql://admin1:ASqw12@localhost:5434/admin1"
# DATABASE_URL = "postgresql://admin1:ASqw12@172.17.0.2:5432/admin1"
DATABASE_URL = "postgresql://postgres:postgres@final_task-postgres-1:5432/postgres"
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5454/admin1"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionType = Type[SessionLocal]

def get_db() -> Generator[SessionType, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
