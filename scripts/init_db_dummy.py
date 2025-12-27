import sys
import os
# Add the project root to python path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app.db import session, models, crud
from app.schemas import alert as alert_schema

def init_db():
    from app.db.session import engine
    models.Base.metadata.create_all(bind=engine)
    
    db = session.SessionLocal()
    
    print("Creating dummy data...")
    
    # Create Alert
    mock_alert_data = {
        "source": "Workstation-01",
        "severity": "Medium",
        "explanation": "Suspicious PowerShell execution detected.",
        "mitre_ttp": "T1059.001",
        "status": "Open"
    }
    # Using the ORM model directly for simplicity in seed script or Pydantic if preferred
    # crud.create_alert expects schema, so let's mock strictly or just use model
    db_alert = models.Alert(**mock_alert_data)
    db.add(db_alert)
    db.commit()
    print(f"Created Alert: {db_alert.id} - {db_alert.explanation}")

    # Create User
    crud.create_user(db, {"email": "analyst@microsoc.io", "role": "Admin", "phone": "+1234567890"})
    print("Created Admin User")

    db.close()

if __name__ == "__main__":
    init_db()
