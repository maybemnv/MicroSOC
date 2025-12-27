from unittest.mock import patch
from app.core.config import settings

def test_ingest_log(client):
    log_payload = {
        "hostname": "server-01",
        "log_file": "/var/log/auth.log",
        "log_message": "Failed password for invalid user admin",
        "timestamp": "2023-10-27T10:00:00"
    }
    
    # Mock the Gemini service analysis
    mock_analysis = {
        "is_threat": True,
        "severity": "Medium",
        "mitre_ttp": "T1110",
        "explanation": "Brute force attempt",
        "confidence": 90
    }
    
    with patch("app.services.gemini_service.analyze_log_with_gemini", return_value=mock_analysis):
        response = client.post(
            f"{settings.API_V1_STR}/logs/ingest",
            json=log_payload
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ingested"
    assert "alert_id" in data
    assert data["analysis"]["severity"] == "Medium"

def test_analyze_log_direct(client):
    log_payload = {
        "hostname": "server-01",
        "log_file": "/var/log/syslog",
        "log_message": "USB device inserted",
    }
    
    mock_analysis = {
        "is_threat": False,
        "severity": "Low",
        "mitre_ttp": None,
        "explanation": "Routine event",
        "confidence": 100
    }
    
    with patch("app.services.gemini_service.analyze_log_with_gemini", return_value=mock_analysis):
        response = client.post(
            f"{settings.API_V1_STR}/logs/analyze",
            json=log_payload
        )
        
    assert response.status_code == 200
    assert response.json() == mock_analysis
