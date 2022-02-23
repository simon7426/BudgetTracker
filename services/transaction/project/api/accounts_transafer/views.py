from decimal import Decimal

from flask import current_app, request
from flask_restx import Namespace, Resource, ValidationError, fields
from werkzeug.exceptions import NotFound

from project.api.accounts_transafer.crud import (
    get_account_transfer_by_id,
    get_account_transfer_by_user_id,
)
from project.api.accounts_transafer.utils import (
    add_account_transfer_handler,
    delete_account_transfer_handler,
    update_account_transfer_handler,
)
from project.api.decorator import token_required

account_transfer_namespace = Namespace("Account Transfer")

account_transfer = account_transfer_namespace.model(
    "Account Transfer",
    {
        "id": fields.Integer(readOnly=True),
        "from_account_id": fields.Integer(required=True),
        "to_account_id": fields.Integer(required=True),
        "transfer_amount": fields.Fixed(decimals=2),
        "created_at": fields.DateTime(readOnly=True),
        "updated_at": fields.DateTime(readOnly=True),
    },
)

parser = account_transfer_namespace.parser()
parser.add_argument("Authorization", location="headers")


@account_transfer_namespace.route("", endpoint="account-transfer-list")
class AccountTransferList(Resource):
    @token_required
    @account_transfer_namespace.expect(parser, validate=True)
    @account_transfer_namespace.marshal_with(
        account_transfer, as_list=True, code=200, description="Success"
    )
    @account_transfer_namespace.response(400, "Operation Error")
    @account_transfer_namespace.response(404, "Not Found")
    def get(self):
        """Get all account transfers for an user"""
        try:
            user_id = AccountTransferList.get.owner_id
            transfer_list = get_account_transfer_by_user_id(user_id)
            if transfer_list:
                return transfer_list, 200
            else:
                raise NotFound
        except NotFound:
            account_transfer_namespace.abort(404, "Not Found")
        except Exception as e:
            current_app.logger.info(e)
            account_transfer_namespace.abort(404, "Operation Error")

    @token_required
    @account_transfer_namespace.expect(account_transfer, parser, validate=True)
    @account_transfer_namespace.marshal_with(
        account_transfer, code=201, description="Success"
    )
    @account_transfer_namespace.response(400, "Operation error")
    @account_transfer_namespace.response(403, "Input payload validation failed")
    def post(self):
        """Add an account transfer transaction"""
        try:
            post_data = request.get_json()
            from_account_id = post_data.get("from_account_id")
            to_account_id = post_data.get("to_account_id")
            transfer_amount = Decimal(post_data.get("transfer_amount"))
            account_owner = AccountTransferList.post.owner_id
            transfer = add_account_transfer_handler(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                transfer_amount=transfer_amount,
                account_owner=account_owner,
            )
            return transfer, 200
        except ValidationError:
            account_transfer_namespace.abort(403, "Input payload validation failed")
        except Exception as e:
            current_app.logger.info(e)
            account_transfer_namespace.abort(400, "Operation error")


@account_transfer_namespace.route("/<int:id>", endpoint="account-transfer")
class AccountTransfer(Resource):
    @token_required
    @account_transfer_namespace.expect(parser, validate=True)
    @account_transfer_namespace.marshal_with(
        account_transfer, code=200, description="success"
    )
    @account_transfer_namespace.response(400, "Operation error")
    @account_transfer_namespace.response(404, "Transfer record <id> does not exists.")
    def get(self, id):
        """Get account transfer by id"""
        try:
            user_id = AccountTransfer.get.owner_id
            transfer = get_account_transfer_by_id(id=id, user_id=user_id)
            if transfer:
                return transfer, 200
            else:
                raise NotFound
        except NotFound:
            account_transfer_namespace.abort(
                404, f"Transfer record {id} does not exists."
            )
        except Exception as e:
            current_app.logger.info(e)
            account_transfer_namespace.abort(400, "Operation error")

    @token_required
    @account_transfer_namespace.expect(account_transfer, parser, validate=True)
    @account_transfer_namespace.marshal_with(
        account_transfer, code=200, description="Success"
    )
    @account_transfer_namespace.response(400, "Operation error")
    @account_transfer_namespace.response(403, "Input payload validation failed")
    @account_transfer_namespace.response(404, "Transfer record <id> does not exists.")
    def put(self, id):
        """Update an account transfer"""
        try:
            put_data = request.get_json()
            from_account_id = put_data.get("from_account_id")
            to_account_id = put_data.get("to_account_id")
            transfer_amount = Decimal(put_data.get("transfer_amount"))
            account_owner = AccountTransfer.put.owner_id
            transfer = get_account_transfer_by_id(id=id, user_id=account_owner)
            if transfer:
                transfer = update_account_transfer_handler(
                    transfer=transfer,
                    from_account_id=from_account_id,
                    to_account_id=to_account_id,
                    transfer_amount=transfer_amount,
                    account_owner=account_owner,
                )
                return transfer, 200
            else:
                raise NotFound
        except ValidationError:
            account_transfer_namespace.abort(403, "Input payload validation failed")
        except NotFound:
            account_transfer_namespace.abort(
                404, f"Transfer record {id} does not exists."
            )
        except Exception as e:
            current_app.logger.info(e)
            account_transfer_namespace.abort(400, "Operation error")

    @token_required
    @account_transfer_namespace.expect(parser, validate=True)
    @account_transfer_namespace.response(204, "No Content")
    @account_transfer_namespace.response(400, "Operation error")
    @account_transfer_namespace.response(404, "Transfer record <id> does not exists.")
    def delete(self, id):
        """Delete an account transfer"""
        try:
            user_id = AccountTransfer.delete.owner_id
            transfer = get_account_transfer_by_id(id=id, user_id=user_id)
            if transfer:
                transfer = delete_account_transfer_handler(transfer)
                return "", 204
            else:
                raise NotFound
        except NotFound:
            account_transfer_namespace.abort(
                404, f"Transfer record {id} does not exists."
            )
        except Exception as e:
            current_app.logger.info(e)
            account_transfer_namespace.abort(400, "Operation error")
