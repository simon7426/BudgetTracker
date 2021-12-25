import enum
import os

from flask_admin.contrib.sqla import ModelView

from project import db
from project.api.utils import get_bd_time


class ChoiceType(enum.Enum):
    income = "income"
    expense = "expense"


class TransactionCategory(db.Model):
    __tablename__ = "transaction_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(128), nullable=False)
    category_type = db.Column(db.Enum(ChoiceType), nullable=False)
    category_owner = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=get_bd_time(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=get_bd_time())

    transactions = db.relationship(
        "TransactionList", backref="transaction_category", lazy=True
    )

    def __init__(self, category_name, category_type, category_owner):
        self.category_name = category_name
        self.category_type = category_type
        self.category_owner = category_owner

    def __repr__(self):
        return "Category: " + self.category_name


class TransactionList(db.Model):
    __tablename__ = "transaction_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_owner = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.Enum(ChoiceType), nullable=False)
    transaction_description = db.Column(db.String(300), nullable=False)
    transaction_cost = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_category_id = db.Column(
        db.Integer, db.ForeignKey("transaction_category.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=get_bd_time(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=get_bd_time())

    def __init__(
        self,
        transaction_owner,
        transaction_type,
        transaction_description,
        transaction_cost,
        transaction_category_id,
    ):
        self.transaction_owner = transaction_owner
        self.transaction_type = transaction_type
        self.transaction_description = transaction_description
        self.transaction_cost = transaction_cost
        self.transaction_category_id = transaction_category_id

    def __repr__(self):
        return f"{self.transaction_type}: {self.transaction_description} {self.transaction_cost}"


if os.getenv("FLASK_ENV") == "development":  # pragma: no cover
    from project import admin

    admin.add_view(ModelView(TransactionCategory, db.session))
    admin.add_view(ModelView(TransactionList, db.session))
