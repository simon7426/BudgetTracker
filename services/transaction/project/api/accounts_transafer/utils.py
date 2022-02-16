from flask_restx import ValidationError

from project.api.accounts.crud import get_account_by_id
from project.api.accounts_transafer.crud import (
    add_account_transfer,
    delete_account_transfer,
    rollback_database,
    update_account_transfer,
)


def add_account_transfer_handler(
    from_account_id, to_account_id, transfer_amount, account_owner
):
    from_account = get_account_by_id(id=from_account_id, account_owner=account_owner)
    to_account = get_account_by_id(id=to_account_id, account_owner=account_owner)
    if (
        from_account
        and to_account
        and transfer_amount > 0.00
        and from_account.account_balance >= transfer_amount
    ):
        from_account.account_balance -= transfer_amount
        to_account.account_balance += transfer_amount
        transfer = add_account_transfer(
            from_account_id, to_account_id, transfer_amount, account_owner
        )
        return transfer
    else:
        raise ValidationError


def update_account_transfer_handler(
    transfer, from_account_id, to_account_id, transfer_amount, account_owner
):
    old_from_account = get_account_by_id(
        id=transfer.from_account_id, account_owner=account_owner
    )
    old_to_account = get_account_by_id(
        id=transfer.to_account_id, account_owner=account_owner
    )
    from_account = get_account_by_id(id=from_account_id, account_owner=account_owner)
    to_account = get_account_by_id(id=to_account_id, account_owner=account_owner)
    old_transfer_amount = transfer.transfer_amount
    if (
        old_from_account
        and old_to_account
        and from_account
        and to_account
        and transfer_amount > 0.00
    ):
        old_from_account.account_balance += old_transfer_amount
        old_to_account.account_balance -= old_transfer_amount
        if from_account.account_balance >= transfer_amount:
            from_account.account_balance -= transfer_amount
            to_account.account_balance += transfer_amount
            updated_transfer = update_account_transfer(
                transfer, from_account_id, to_account_id, transfer_amount, account_owner
            )
            return updated_transfer
        else:
            rollback_database()
            raise ValidationError
    else:
        raise ValidationError


def delete_account_transfer_handler(transfer):
    transfer_amount = transfer.transfer_amount
    transfer.from_account.account_balance += transfer_amount
    transfer.to_account.account_balance -= transfer_amount
    transfer = delete_account_transfer(transfer)
    return transfer
