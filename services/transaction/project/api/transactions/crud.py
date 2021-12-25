from project import db

from project.api.transactions.models import (  # isort:skip
    TransactionCategory,
    TransactionList,
)


def get_all_transaction_category(owner_id):
    return TransactionCategory.query.filter_by(category_owner=owner_id).all()


def get_transaction_category(id, owner_id):
    return TransactionCategory.query.filter_by(id=id, category_owner=owner_id).first()


def add_category(category_name, category_type, category_owner):
    category = TransactionCategory(
        category_name=category_name,
        category_type=category_type,
        category_owner=category_owner,
    )
    db.session.add(category)
    db.session.commit()
    return category


def update_category(category, category_name, category_type):
    
    category.category_name = category_name
    category.category_type = category_type
    db.session.commit()
    return category


def delete_category(category):
    db.session.delete(category)
    db.session.commit()
    return None


def get_all_transactions(owner_id):
    return TransactionList.query.filter_by(transaction_owner=owner_id).all()


def get_transaction(id, owner_id):
    return TransactionList.query.filter_by(id=id, transaction_owner=owner_id).first()


def add_transaction(
    transaction_owner,
    transaction_type,
    transaction_description,
    transaction_cost,
    transaction_category_id,
):
    transaction = TransactionList(
        transaction_owner=transaction_owner,
        transaction_type=transaction_type,
        transaction_description=transaction_description,
        transaction_cost=transaction_cost,
        transaction_category_id=transaction_category_id,
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction


def update_transaction(
    transaction,
    transaction_owner,
    transaction_type,
    transaction_description,
    transaction_cost,
    transaction_category_id,
):
    transaction.transaction_owner = transaction_owner
    transaction.transaction_type = (transaction_type,)
    transaction.transaction_description = (transaction_description,)
    transaction.transaction_cost = (transaction_cost,)
    transaction.transaction_category_id = transaction_category_id
    db.session.commit()
    return transaction


def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()
    return None
