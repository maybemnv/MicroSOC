from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import gemini_service
from app.db import session, crud, models
from pydantic import BaseModel

router = APIRouter()

class LogIngest(BaseModel):
    event: str
    hostname: str
    file: str
    entropy: float
    source_ip: str = "127.0.0.1"

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest")
def ingest_log(log: LogIngest, db: Session = Depends(get_db)):
    # 1. Ingest/Analyze (Real Gemini Analysis)
    analysis_result = gemini_service.analyze_log_with_gemini(log.dict())
    
    # 2. Store Alert
    alert_data = {
        "source": log.hostname,
        "severity": analysis_result.get("severity", "Low"),
        "explanation": analysis_result.get("explanation", "No explanation provided."),
        "mitre_ttp": analysis_result.get("mitre_ttp"),
        "status": "Open"
    }
    # Using model directly for speed, or could use schema
    alert = crud.create_alert(db=db, alert=models.Alert(**alert_data))
    
    return {"status": "ingested", "alert_id": alert.id, "analysis": analysis_result}

@router.post("/analyze")
def analyze_log_endpoint(log: LogIngest):
    """Direct analysis endpoint (stateless)"""
    return gemini_service.analyze_log_with_gemini(log.dict())
