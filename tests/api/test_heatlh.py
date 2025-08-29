def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.get_json()["message"] == "pong"
