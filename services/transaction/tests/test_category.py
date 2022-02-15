import json

import pytest

import project.api.transaction_categories.views
from project.api.models import TransactionCategory


def test_categories_001_add_category(test_app, test_database, test_token):
    client = test_app.test_client()
    resp = client.post(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(
            {
                "category_name": "test01",
                "category_type": "income",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "id" in data
    assert "test01" == data["category_name"]
    assert "income" == data["category_type"]


@pytest.mark.parametrize(
    "payload, status_code, message",
    [
        [{}, 400, "Input payload validation failed"],
        [{"category_name": "test01"}, 400, "Input payload validation failed"],
        [
            {"category_name": "test01", "category_type": "invalid"},
            400,
            "Input payload validation failed",
        ],
    ],
)
def test_category_002_add_category_invalid_json(
    test_app, test_database, test_token, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.post(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_categories_003_add_category_exception(
    test_app, test_database, test_token, monkeypatch
):
    def mock_add_category(category_name, category_type, category_owner):
        raise Exception

    monkeypatch.setattr(
        project.api.transaction_categories.views, "add_category", mock_add_category
    )
    client = test_app.test_client()
    resp = client.post(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(
            {
                "category_name": "test01",
                "category_type": "income",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Unable to create category" in data["message"]


def test_category_004_get_all_categories(
    test_app, test_database, test_token, add_category
):
    test_database.session.query(TransactionCategory).delete()
    category1 = add_category("test01", "income", 1)
    add_category("test02", "expense", 2)
    category3 = add_category("test03", "expense", 1)
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]["category_name"] == category1.category_name
    assert data[1]["category_name"] == category3.category_name
    assert data[0]["category_type"] == category1.category_type.value
    assert data[1]["category_type"] == category3.category_type.value


def test_categories_005_get_all_categories_exception(
    test_app, test_database, test_token, monkeypatch
):
    def mock_get_all_transaction_category(owner_id):
        raise Exception

    monkeypatch.setattr(
        project.api.transaction_categories.views,
        "get_all_transaction_category",
        mock_get_all_transaction_category,
    )
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Unable to fetch categories." in data["message"]


def test_categories_006_test_single_category(
    test_app, test_database, test_token, add_category
):
    category1 = add_category("test01", "income", 1)
    client = test_app.test_client()
    resp = client.get(
        f"/api/v1/transactions-service/category/{category1.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert data["category_name"] == category1.category_name
    assert data["category_type"] == category1.category_type.value


def test_categories_007_test_single_category_no_such_category(
    test_app, test_database, test_token
):
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions-service/category/999",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "No Such Category" in data["message"]


def test_categories_008_test_single_category_invalid_owner(
    test_app, test_database, test_token, add_category
):
    category1 = add_category("test01", "income", 2)
    client = test_app.test_client()
    resp = client.get(
        f"/api/v1/transactions-service/category/{category1.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "No Such Category" in data["message"]


def test_categories_009_test_single_category_exception(
    test_app, test_database, test_token, add_category, monkeypatch
):
    def mock_get_transaction_category(id, owner_id):
        raise Exception

    monkeypatch.setattr(
        project.api.transaction_categories.views,
        "get_transaction_category",
        mock_get_transaction_category,
    )
    category1 = add_category("test01", "income", 1)
    client = test_app.test_client()
    resp = client.get(
        f"/api/v1/transactions-service/category/{category1.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Operation Error" in data["message"]


def test_categories_010_update_category(
    test_app, test_database, test_token, add_category
):
    test_database.session.query(TransactionCategory).delete()
    category1 = add_category("test01", "income", 1)
    client = test_app.test_client()
    resp = client.put(
        f"/api/v1/transactions-service/category/{category1.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(
            {"category_name": "test_01_updated", "category_type": "expense"}
        ),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data["id"] == category1.id
    assert data["category_name"] == "test_01_updated"
    assert data["category_type"] == "expense"
    resp = client.get(
        f"/api/v1/transactions-service/category/{category1.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data["id"] == category1.id
    assert data["category_name"] == "test_01_updated"
    assert data["category_type"] == "expense"


@pytest.mark.parametrize(
    "payload, status_code, message",
    [
        [{}, 400, "Input payload validation failed"],
        [{"category_name": "updated"}, 400, "Input payload validation failed"],
        [
            {"category_name": "updated", "category_type": "lol"},
            400,
            "Input payload validation failed",
        ],
    ],
)
def test_categories_011_update_category_invalid_operation(
    test_app, test_database, test_token, add_category, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions-service/category",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    id = data[0]["id"]
    resp = client.put(
        f"/api/v1/transactions-service/category/{id}",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == status_code
    data = json.loads(resp.data.decode())
    assert data["message"] == message


def test_categories_012_update_category_invalid_owner(
    test_app, test_database, test_token, add_category
):
    category = add_category("test_invalid_owner", "income", 2)
    client = test_app.test_client()
    resp = client.put(
        f"/api/v1/transactions-service/category/{category.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(
            {
                "category_name": "valid_owner",
                "category_type": "expense",
            }
        ),
        content_type="application/json",
    )
    assert resp.status_code == 404
    data = json.loads(resp.data.decode())
    assert data["message"] == "No Such Category"


def test_categories_013_update_category_exception(
    test_app, test_database, test_token, add_category, monkeypatch
):
    def mock_update_category(category, catogory_name, category_type):
        raise Exception

    monkeypatch.setattr(
        project.api.transaction_categories.views,
        "update_category",
        mock_update_category,
    )
    category = add_category("test_exception", "income", 1)
    client = test_app.test_client()
    resp = client.put(
        f"/api/v1/transactions-service/category/{category.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        data=json.dumps(
            {
                "category_name": "test_exception_updated",
                "category_type": "expense",
            }
        ),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert data["message"] == "Operation Error"


def test_categories_014_delete_category(
    test_app, test_database, test_token, add_category
):
    category = add_category("test_delete", "income", 1)
    client = test_app.test_client()
    resp = client.delete(
        f"/api/v1/transactions-service/category/{category.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    assert resp.status_code == 204


def test_categories_015_delete_category_invalid_owner(
    test_app, test_database, test_token, add_category
):
    category = add_category("test_delete", "income", 2)
    client = test_app.test_client()
    resp = client.delete(
        f"/api/v1/transactions-service/category/{category.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    assert resp.status_code == 404
    data = json.loads(resp.data.decode())
    assert data["message"] == "No Such Category"


def test_categories_016_delete_category_invalid_owner(
    test_app, test_database, test_token, add_category, monkeypatch
):
    def mock_delete_category(category):
        raise Exception

    monkeypatch.setattr(
        project.api.transaction_categories.views,
        "delete_category",
        mock_delete_category,
    )
    category = add_category("test_delete", "income", 1)
    client = test_app.test_client()
    resp = client.delete(
        f"/api/v1/transactions-service/category/{category.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert data["message"] == "Operation Error"
