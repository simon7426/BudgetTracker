from decimal import Decimal

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

from project.api.accounts.crud import (
    add_account,
    delete_account,
    get_account_by_id,
    get_all_accounts_by_user_id,
    update_account,
)
from project.api.decorator import token_required

account_namespace = Namespace("Accounts")

parser = account_namespace.parser()
parser.add_argument("Authorization", location="headers")


account_model = account_namespace.model(
    "Accounts",
    {
        "id": fields.Integer(readOnly=True),
        "account_name": fields.String(required=True),
        "account_type": fields.String(required=True),
        "account_balance": fields.Fixed(decimals=2, required=True),
        "created_at": fields.DateTime(readOnly=True),
        "updated_at": fields.DateTime(readOnly=True),
    },
)


@account_namespace.route("", endpoint="accounts-list")
class AccountsList(Resource):
    @token_required
    @account_namespace.expect(parser, validate=True)
    @account_namespace.marshal_with(
        account_model, as_list=True, code=200, description="Success"
    )
    @account_namespace.response(400, "Operation error")
    @account_namespace.response(401, "Invalid Token")
    @account_namespace.response(404, "No accounts found.")
    def get(self):
        """Get all the accounts of an user"""
        try:
            user_id = AccountsList.get.owner_id
            accounts = get_all_accounts_by_user_id(user_id)
            return accounts, 200
        except Exception as e:
            current_app.logger.info(e)
            account_namespace.abort(400, "Operation error")

    @token_required
    @account_namespace.expect(parser, account_model, validate=True)
    @account_namespace.marshal_with(account_model, code=201, description="Created")
    @account_namespace.response(400, "Operation error.")
    @account_namespace.response(401, "Invalid Token")
    def post(self):
        """Add an account for an user"""
        try:
            user_id = AccountsList.post.owner_id
            post_data = request.get_json()
            account_name = post_data.get("account_name")
            account_type = post_data.get("account_type")
            account_balance = Decimal(post_data.get("account_balance"))
            account_owner = user_id
            account = add_account(
                account_name=account_name,
                account_type=account_type,
                account_balance=account_balance,
                account_owner=account_owner,
            )
            return account, 201
        except Exception as e:
            current_app.logger.info(e)
            account_namespace.abort(400, "Operation error.")


@account_namespace.route("/<int:id>", endpoint="accounts")
class Accounts(Resource):
    @token_required
    @account_namespace.expect(parser, validate=True)
    @account_namespace.marshal_with(account_model, code=200, description="Success")
    @account_namespace.response(400, "Operation error")
    @account_namespace.response(401, "Invalid Token")
    @account_namespace.response(404, "Account <id> does not exists")
    def get(self, id):
        """Retrive an account"""
        try:
            user_id = Accounts.get.owner_id
            account = get_account_by_id(id=id, account_owner=user_id)
            if account:
                return account, 200
            else:
                raise NotFound
        except NotFound:
            account_namespace.abort(404, f"Account {id} does not exists")
        except Exception as e:
            current_app.logger.info(e)
            account_namespace.abort(400, "Operation error")

    @token_required
    @account_namespace.expect(parser, account_model, validate=True)
    @account_namespace.marshal_with(account_model, code=200, description="Success")
    @account_namespace.response(400, "Operation error")
    @account_namespace.response(401, "Invalid Token")
    @account_namespace.response(404, "Account <id> does not exists")
    def put(self, id):
        """Update an account"""
        try:
            user_id = Accounts.put.owner_id
            account = get_account_by_id(id=id, account_owner=user_id)
            if account:
                put_data = request.get_json()
                account_name = put_data.get("account_name")
                account_type = put_data.get("account_type")
                account_balance = put_data.get("account_balance")
                account = update_account(
                    account, account_name, account_type, account_balance
                )
                return account, 200
            else:
                raise NotFound
        except NotFound:
            account_namespace.abort(404, f"Account {id} does not exists")
        except Exception as e:
            current_app.logger.info(e)
            account_namespace.abort(400, "Operation error")

    @token_required
    @account_namespace.expect(parser, validate=True)
    @account_namespace.response(204, "No content")
    @account_namespace.response(400, "Operation error")
    @account_namespace.response(401, "Invalid Token")
    @account_namespace.response(404, "Account <id> does not exists")
    def delete(self, id):
        """Delete an account"""
        try:
            user_id = Accounts.put.owner_id
            account = get_account_by_id(id=id, account_owner=user_id)
            if account:
                delete_account(account)
                return "", 204
            else:
                raise NotFound
        except NotFound:
            account_namespace.abort(404, f"Account {id} does not exists")
        except Exception as e:
            current_app.logger.info(e)
            account_namespace.abort(400, "Operation error")
