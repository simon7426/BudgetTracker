import json

import pytest

import project.api.transactions.apis
from project.api.transactions.models import TransactionCategory


def test_categories_001_add_category(test_app, test_database, test_token):
    client = test_app.test_client()
    resp = client.post(
        "/api/v1/transactions/category",
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
        "/api/v1/transactions/category",
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
        project.api.transactions.apis, "add_category", mock_add_category
    )
    client = test_app.test_client()
    resp = client.post(
        "/api/v1/transactions/category",
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
        "/api/v1/transactions/category",
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
        project.api.transactions.apis,
        "get_all_transaction_category",
        mock_get_all_transaction_category,
    )
    client = test_app.test_client()
    resp = client.get(
        "/api/v1/transactions/category",
        headers={"Authorization": f"Bearer {test_token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Unable to fetch categories." in data["message"]


# def test_packages_004_single_package(test_app, test_database, add_package):
#     package = add_package("test01", 1, 100)
#     client = test_app.test_client()
#     resp = client.get(f"/package/{package.id}")
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 200
#     assert "test01" in data["package_name"]
#     assert data["package_size"] == 1
#     assert data["package_price"] == 100


# def test_packages_005_single_user_incorrect_id(test_app, test_database):
#     client = test_app.test_client()
#     resp = client.get("/package/999")
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 404
#     assert "Package 999 does not exist" in data["message"]


# def test_packages_006_all_packages(test_app, test_database, add_package):
#     test_database.session.query(Package).delete()
#     add_package("test01", 1, 100)
#     add_package("test02", 2, 180)
#     client = test_app.test_client()
#     resp = client.get("/package")
#     resp_data = json.loads(resp.data.decode())
#     data = resp_data["packages"]
#     assert resp.status_code == 200
#     assert len(data) == 2
#     assert "test01" in data[0]["package_name"]
#     assert data[0]["package_size"] == 1
#     assert data[0]["package_price"] == 100
#     assert "test02" in data[1]["package_name"]
#     assert data[1]["package_size"] == 2
#     assert data[1]["package_price"] == 180


# def test_packages_007_remove_user(test_app, test_database, add_package):
#     test_database.session.query(Package).delete()
#     package = add_package("test01", 1, 100)
#     client = test_app.test_client()
#     resp_one = client.get("/package")
#     resp_data = json.loads(resp_one.data.decode())
#     data = resp_data["packages"]
#     assert resp_one.status_code == 200
#     assert len(data) == 1

#     resp_two = client.delete(f"/package/{package.id}")
#     assert resp_two.status_code == 204

#     resp_three = client.get("/package")
#     resp_data = json.loads(resp_three.data.decode())
#     data = resp_data["packages"]
#     assert resp_three.status_code == 200
#     assert len(data) == 0


# def test_packages_008_remove_user_incorrect_id(test_app, test_database):
#     client = test_app.test_client()
#     resp = client.delete("/package/999")
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 404
#     assert "Package 999 does not exist" in data["message"]


# def test_packages_009_update_user(test_app, test_database, add_package):
#     package = add_package("test01", 1, 100)
#     client = test_app.test_client()
#     resp_one = client.put(
#         f"/package/{package.id}",
#         data=json.dumps(
#             {
#                 "package_name": "test01_updated",
#                 "package_size": 1,
#                 "package_price": 120,
#             }
#         ),
#         content_type="application/json",
#     )
#     data = json.loads(resp_one.data.decode())
#     assert resp_one.status_code == 200
#     assert f"{package.id} was updated!" in data["message"]

#     resp_two = client.get(f"/package/{package.id}")
#     data = json.loads(resp_two.data.decode())
#     assert resp_two.status_code == 200
#     assert "test01_updated" in data["package_name"]
#     assert data["package_size"] == 1
#     assert data["package_price"] == 120


# @pytest.mark.parametrize(
#     "package_id, payload, status_code, message",
#     [
#         [1, {}, 400, "Input payload validation failed"],
#         [1, {"package_name": "test01"}, 400, "Input payload validation failed"],
#         [
#             999,
#             {"package_name": "test01", "package_size": 5, "package_price": 1200},
#             404,
#             "Package 999 does not exist",
#         ],
#     ],
# )
# def test_packages_010_update_user_invalid(
#     test_app, test_database, package_id, payload, status_code, message
# ):
#     client = test_app.test_client()
#     resp = client.put(
#         f"/package/{package_id}",
#         data=json.dumps(payload),
#         content_type="application/json",
#     )
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == status_code
#     assert message in data["message"]
