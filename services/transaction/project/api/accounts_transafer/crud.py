from project import db
from project.api.models import AccountTransfer


def get_account_transfer_by_user_id(user_id):
    return (
        AccountTransfer.query.filter_by(account_owner=user_id)
        .order_by(AccountTransfer.id.desc())
        .all()
    )


def get_account_transfer_by_id(id, user_id):
    return AccountTransfer.query.filter_by(id=id, account_owner=user_id).first()


def add_account_transfer(
    from_account_id, to_account_id, transfer_amount, account_owner, transfer_description
):
    transfer = AccountTransfer(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        transfer_amount=transfer_amount,
        account_owner=account_owner,
        transfer_description=transfer_description,
    )
    db.session.add(transfer)
    db.session.commit()
    return transfer


def update_account_transfer(
    transfer,
    from_account_id,
    to_account_id,
    transfer_amount,
    account_owner,
    transfer_description,
):
    transfer.from_account_id = from_account_id
    transfer.to_account_id = to_account_id
    transfer.transfer_amount = transfer_amount
    transfer.account_owner = account_owner
    transfer.transfer_description = transfer_description
    db.session.commit()
    return transfer


def delete_account_transfer(transfer):
    db.session.delete(transfer)
    db.session.commit()
    return transfer


def rollback_database():
    db.session.rollback()
