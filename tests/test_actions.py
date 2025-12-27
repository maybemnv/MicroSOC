from app.core.config import settings

def test_perform_action(client):
    response = client.post(
        f"{settings.API_V1_STR}/actions/",
        json={"alert_id": 1, "action": "block_ip"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "executed", "action": "block_ip", "alert_id": 1, "success": True}

def test_make_decision(client):
    response = client.post(f"{settings.API_V1_STR}/actions/decision?alert_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_action" in data
    assert "confidence" in data
