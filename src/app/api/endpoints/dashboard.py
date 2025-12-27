from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import session, crud
from app.api.deps import get_db

router = APIRouter()

@router.get("/incidents")
def get_incidents(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    alerts = crud.get_alerts(db, skip=skip, limit=limit)
    return alerts
