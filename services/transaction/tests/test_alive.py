import json


def test_alive_001_test_alive(test_app):
    client = test_app.test_client()
    resp = client.get("/alive")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Alive" in data["message"]
