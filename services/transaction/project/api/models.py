import enum

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
    transaction_account_id = db.Column(
        db.Integer, db.ForeignKey("transaction_account.id"), nullable=False
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
        transaction_account_id,
    ):
        self.transaction_owner = transaction_owner
        self.transaction_type = transaction_type
        self.transaction_description = transaction_description
        self.transaction_cost = transaction_cost
        self.transaction_category_id = transaction_category_id
        self.transaction_account_id = transaction_account_id

    def __repr__(self):
        return f"{self.transaction_type}: {self.transaction_description} {self.transaction_cost}"


class Account(db.Model):
    __tablename__ = "transaction_account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_name = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(128), nullable=False)
    account_balance = db.Column(db.Numeric(10, 2), nullable=False)
    account_owner = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=get_bd_time(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=get_bd_time())

    transactions = db.relationship(
        "TransactionList", backref="transaction_account", lazy=True
    )

    def __init__(self, account_name, account_type, account_balance, account_owner):
        self.account_name = account_name
        self.account_type = account_type
        self.account_balance = account_balance
        self.account_owner = account_owner

    def __repr__(self):
        return f"Account: {self.account_name}"


class AccountTransfer(db.Model):
    __tablename__ = "transaction_account_transfer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_account_id = db.Column(
        db.Integer, db.ForeignKey("transaction_account.id"), nullable=False
    )
    from_account = db.relationship("Account", foreign_keys=[from_account_id])
    to_account_id = db.Column(
        db.Integer, db.ForeignKey("transaction_account.id"), nullable=False
    )
    to_account = db.relationship("Account", foreign_keys=[to_account_id])
    transfer_cost = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=get_bd_time(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=get_bd_time())

    def __init__(self, from_account_id, to_account_id, transfer_cost):
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.transfer_cost = transfer_cost

    def __repr__(self):
        return f"Transfer: from {self.from_account.account_name} to {self.to_account.account_name}"
