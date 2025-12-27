from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ActionRequest(BaseModel):
    alert_id: int
    action: str

@router.post("/")
def perform_action(req: ActionRequest):
    # Stub: "Performing action..."
    return {"status": "executed", "action": req.action, "alert_id": req.alert_id, "success": True}

@router.post("/decision")
def make_decision(alert_id: int):
    # Stub: ADK decision
    return {"recommended_action": "isolate_host", "confidence": 0.95}
