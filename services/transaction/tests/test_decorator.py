from datetime import datetime, timedelta

from flask import current_app, json

from project.api.utils import generate_token_for_test


def test_decorator_001_valid_token(test_app, test_database, add_category):
    add_category("test01", "income", 1)
    client = test_app.test_client()
    token = generate_token_for_test(
        1,
        "member",
        "access",
        datetime.utcnow() + timedelta(minutes=5),
        current_app.config.get("SECRET_KEY"),
    )
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 1


def test_decorator_002_invalid_token(test_app, test_database, add_category):
    add_category("test01", "income", 1)
    client = test_app.test_client()
    token = "INVALID_TOKEN"
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Invalid Token" in data["message"]


def test_decorator_003_empty_header(test_app, test_database, add_category):
    add_category("test01", "income", 1)
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions-service/category",
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Invalid Token" in data["message"]


def test_decorator_004_invalid_token_type(test_app, test_database, add_category):
    add_category("test01", "income", 1)
    client = test_app.test_client()
    token = generate_token_for_test(
        1,
        "member",
        "refresh",
        datetime.utcnow() + timedelta(minutes=5),
        current_app.config.get("SECRET_KEY"),
    )
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Invalid Token" in data["message"]


def test_decorator_005_expired_token(test_app, test_database, add_category):
    add_category("test01", "income", 1)
    client = test_app.test_client()
    token = generate_token_for_test(
        1,
        "member",
        "access",
        datetime.utcnow() - timedelta(minutes=5),
        current_app.config.get("SECRET_KEY"),
    )
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Token Expired" in data["message"]
