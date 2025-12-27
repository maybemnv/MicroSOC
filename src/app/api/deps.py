from typing import Generator
from app.db import session

def get_db() -> Generator:
    try:
        db = session.SessionLocal()
        yield db
    finally:
        db.close()
