from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import gemini_service, decision_engine

from app.schemas.log import LogIngest
from app.schemas.alert import AlertCreate
from app.db import models, crud
from app.api.deps import get_db


router = APIRouter()

@router.post("/ingest")
def ingest_log(log: LogIngest, db: Session = Depends(get_db)):
    # 1. Ingest/Analyze (Real Gemini Analysis)
    analysis_result = gemini_service.analyze_log_with_gemini(log.model_dump())
    
    # 2. Store Alert
    alert_data = {
        "source": log.hostname,
        "severity": analysis_result.get("severity", "Low"),
        "explanation": analysis_result.get("explanation", "No explanation provided."),
        "mitre_ttp": analysis_result.get("mitre_ttp"),
        "status": "Open"
    }
    alert = crud.create_alert(db=db, alert=AlertCreate(**alert_data))
    
    # 3. Automated Decision & Response (ADK)
    # If High Severity, we trigger the agent immediately
    decision_result = None
    if alert.severity == "High":
        decision_result = decision_engine.run_automated_response(db, alert.id)
    
    return {
        "status": "ingested", 
        "alert_id": alert.id, 
        "analysis": analysis_result,
        "automated_response": decision_result
    }

@router.post("/analyze")
def analyze_log_endpoint(log: LogIngest):
    """Direct analysis endpoint (stateless)"""
    return gemini_service.analyze_log_with_gemini(log.model_dump())
