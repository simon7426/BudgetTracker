from project import db
from project.api.models import Account


def get_all_accounts_by_user_id(user_id):
    return Account.query.filter_by(account_owner=user_id).all()


def get_account_by_id(id, account_owner):
    return Account.query.filter_by(id=id, account_owner=account_owner).first()


def add_account(account_name, account_type, account_balance, account_owner):
    account = Account(
        account_name=account_name,
        account_type=account_type,
        account_balance=account_balance,
        account_owner=account_owner,
    )
    db.session.add(account)
    db.session.commit()
    return account


def update_account(account, account_name, account_type, account_balance):
    account.account_name = account_name
    account.account_type = account_type
    account.account_balance = account_balance
    db.session.commit()
    return account


def delete_account(account):
    db.session.delete(account)
    db.session.commit()
    return None
