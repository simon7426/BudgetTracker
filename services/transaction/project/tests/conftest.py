import jwt
import pytest
from flask import current_app

from project import create_app, db
from project.api.transactions.models import TransactionCategory


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def test_token():
    payload = {"sub": 1, "role": "member", "type": "access"}
    encoded_token = jwt.encode(
        payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
    )
    yield encoded_token


@pytest.fixture(scope="module")
def add_category():
    def _add_category(category_name, category_type, category_owner):
        category = TransactionCategory(
            category_name=category_name,
            category_type=category_type,
            category_owner=category_owner,
        )
        db.session.add(category)
        db.session.commit()
        return category

    return _add_category
