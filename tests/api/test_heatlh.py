def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.get_json()["message"] == "pong"

def test_ready(client):
    res = client.get("/ready")
    assert res.status_code == 200
    data = res.get_json()
    assert "provider" in data and "loaded" in data and "dim" in data