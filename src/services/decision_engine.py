from app.db import crud, models
from sqlalchemy.orm import Session
import time

class Responder:
    """Simulates external API calls to firewalls/GSuite"""
    
    @staticmethod
    def block_ip_pfsense(ip: str):
        # Simulation delay
        time.sleep(0.5) 
        return f"Blocked IP {ip} on pfSense firewall."

    @staticmethod
    def disable_user_gsuite(email: str):
        time.sleep(0.5)
        return f"Suspended user {email} in Google Workspace."

class DecisionEngine:
    """
    Autonomous Decision Agent (The 'Orchestrator' logic).
    Evaluates alerts and triggers responses.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def evaluate_and_respond(self, alert_id: int):
        alert = crud.get_alert(self.db, alert_id)
        if not alert:
            return None
            
        decision = {
            "alert_id": alert.id,
            "action_taken": "Monitor",
            "success": True,
            "executor": "ADK_Orchestrator"
        }

        # Logic: If High Severity, AUTOMATE response
        if alert.severity == "High":
            if "Login" in alert.explanation or "Brute" in alert.explanation:
                # Assume extracting IP or User from source/explanation strictly requires better parsing
                # For demo, we simulate a 'block' action
                result = Responder.block_ip_pfsense("1.2.3.4") # Mock IP
                decision["action_taken"] = f"Block IP (Automated): {result}"
                
            elif "Ransomware" in alert.explanation or "Encrypted" in alert.explanation:
                result = Responder.disable_user_gsuite("compromised_user@microsoc.io")
                decision["action_taken"] = f"Disable User (Automated): {result}"
        
        # Save Action to DB
        action_record = {
            "alert_id": decision["alert_id"],
            "action_taken": decision["action_taken"],
            "success": decision["success"],
            "executor": decision["executor"]
        }
        crud.create_action(self.db, action_record)
        
        return decision

def run_automated_response(db: Session, alert_id: int):
    engine = DecisionEngine(db)
    return engine.evaluate_and_respond(alert_id)
