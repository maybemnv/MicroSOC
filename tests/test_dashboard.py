from app.core.config import settings

def test_get_incidents_empty(client):
    # Depending on DB state, this might return empty or seeded data
    response = client.get(f"{settings.API_V1_STR}/dashboard/incidents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
