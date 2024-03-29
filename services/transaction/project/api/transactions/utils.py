from datetime import datetime

from flask_restx import ValidationError

from project.api.accounts.crud import get_account_by_id
from project.api.accounts_transafer.crud import rollback_database
from project.api.transactions.crud import (
    add_transactions,
    delete_transaction,
    update_transaction,
)


def add_transactions_handler(
    transaction_owner,
    transaction_date,
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
):
    account = get_account_by_id(
        id=transaction_account_id, account_owner=transaction_owner
    )
    if account and transaction_amount > 0.00:
        if transaction_type == "expense":
            if account.account_balance >= transaction_amount:
                account.account_balance -= transaction_amount
            else:
                raise ValidationError
        else:
            account.account_balance += transaction_amount
    else:
        raise ValidationError
    transactions = add_transactions(
        transaction_owner=transaction_owner,
        transaction_date=datetime.strptime(transaction_date, "%Y-%m-%d").date(),
        transaction_type=transaction_type,
        transaction_description=transaction_description,
        transaction_amount=transaction_amount,
        transaction_category_id=transaction_category_id,
        transaction_account_id=transaction_account_id,
    )
    return transactions


def delete_transaction_handler(transaction):
    account = get_account_by_id(
        id=transaction.transaction_account_id,
        account_owner=transaction.transaction_owner,
    )
    if transaction.transaction_type.value == "income":
        if account.account_balance >= transaction.transaction_amount:
            account.account_balance -= transaction.transaction_amount
        else:
            raise ValidationError
    else:
        account.account_balance += transaction.transaction_amount
    transaction = delete_transaction(transaction)
    return transaction


def update_transaction_handler(
    transaction,
    transaction_type,
    transaction_date,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
):
    try:
        if transaction.transaction_account_id != transaction_account_id:
            old_account = get_account_by_id(
                id=transaction.transaction_account_id,
                account_owner=transaction.transaction_owner,
            )
            account = get_account_by_id(
                id=transaction_account_id, account_owner=transaction.transaction_owner
            )
            if old_account and account:
                if transaction.transaction_type.value == "income":
                    if old_account.account_balance >= transaction.transaction_amount:
                        old_account.account_balance -= transaction.transaction_amount
                        account.account_balance += transaction_amount
                    else:
                        raise ValidationError
                else:
                    old_account.account_balance += transaction.transaction_amount
                    if account.account_balance >= transaction_amount:
                        account.account_balance -= transaction_amount
                    else:
                        raise ValidationError
            else:
                raise ValidationError
        else:
            account = get_account_by_id(
                id=transaction_account_id, account_owner=transaction.transaction_owner
            )
            if account:
                if transaction.transaction_type.value == "income":
                    account.account_balance = (
                        account.account_balance
                        + transaction_amount
                        - transaction.transaction_amount
                    )
                else:
                    account.account_balance = (
                        account.account_balance
                        - transaction_amount
                        + transaction.transaction_amount
                    )
                if account.account_balance < 0:
                    raise ValidationError
            else:
                raise ValidationError
        transaction = update_transaction(
            transaction=transaction,
            transaction_date=datetime.strptime(transaction_date, "%Y-%m-%d").date(),
            transaction_type=transaction_type,
            transaction_description=transaction_description,
            transaction_amount=transaction_amount,
            transaction_category_id=transaction_category_id,
            transaction_account_id=transaction_account_id,
        )
        return transaction
    except ValidationError:
        rollback_database()
        raise ValidationError
