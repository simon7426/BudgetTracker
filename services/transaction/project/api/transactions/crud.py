from project import db
from project.api.models import TransactionList


def get_all_transactions_by_transaction_owner(transaction_owner, keyset, limit):
    return TransactionList.query.filter(
        TransactionList.transaction_owner == transaction_owner, TransactionList.id <= keyset).order_by(
        TransactionList.id.desc()).limit(limit).all()


def get_transactions_by_id(id, transaction_owner):
    return TransactionList.query.filter_by(
        id=id, transaction_owner=transaction_owner
    ).first()


def add_transactions(
    transaction_owner,
    transaction_date,
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
):
    transactions = TransactionList(
        transaction_owner=transaction_owner,
        transaction_date=transaction_date,
        transaction_type=transaction_type,
        transaction_description=transaction_description,
        transaction_amount=transaction_amount,
        transaction_category_id=transaction_category_id,
        transaction_account_id=transaction_account_id,
    )
    db.session.add(transactions)
    db.session.commit()
    return transactions


def update_transaction(
    transaction,
    transaction_date,
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
):
    transaction.transaction_date = transaction_date
    transaction.transaction_type = transaction_type
    transaction.transaction_description = transaction_description
    transaction.transaction_amount = transaction_amount
    transaction.transaction_category_id = transaction_category_id
    transaction.transaction_account_id = transaction_account_id
    db.session.commit()
    return transaction


def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()
    return transaction
