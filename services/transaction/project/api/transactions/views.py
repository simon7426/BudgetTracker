from flask import current_app, request
from flask_restx import Namespace, Resource, ValidationError, fields
from werkzeug.exceptions import NotFound

from project.api.decorator import token_required
from project.api.models import ChoiceType
from project.api.transactions.crud import (
    get_all_transactions_by_transaction_owner,
    get_transactions_by_id,
)
from project.api.transactions.utils import (
    add_transactions_handler,
    delete_transaction_handler,
    update_transaction_handler,
)

transactions_namespace = Namespace("Transactions")

parser = transactions_namespace.parser()
parser.add_argument("Authorization", location="headers")

query_parser = transactions_namespace.parser()
query_parser.add_argument("keyset", type=int)
query_parser.add_argument("limit", type=int)

transactions = transactions_namespace.model(
    "Transactions",
    {
        "id": fields.Integer(readOnly=True),
        "transaction_date": fields.Date(required=True),
        "transaction_type": fields.String(
            enum=ChoiceType._member_names_,
            attribute="transaction_type.value",
            required=True,
            description="Transaction type",
        ),
        "transaction_description": fields.String(required=True),
        "transaction_amount": fields.Float(requierd=True),
        "transaction_category_id": fields.Integer(required=True),
        "transaction_account_id": fields.Integer(required=True),
        "created_at": fields.DateTime(readOnly=True),
        "updated_at": fields.DateTime(readOnly=True),
    },
)


@transactions_namespace.route("", endpoint="transactions-list")
class TransactionsList(Resource):
    @token_required
    @transactions_namespace.expect(parser, validate=True)
    @transactions_namespace.marshal_with(
        transactions, as_list=True, code=200, description="success"
    )
    @transactions_namespace.response(400, "Operation Error")
    @transactions_namespace.response(404, "Not Found")
    def get(self):
        """Get all transactions for an user"""
        try:
            args = query_parser.parse_args()
            keyset = args["keyset"] if args["keyset"] else 10**9+7
            limit = args["limit"] if args["limit"] else 5

            user_id = TransactionsList.get.owner_id
            transactions_list = get_all_transactions_by_transaction_owner(
                transaction_owner=user_id,
                keyset=keyset,
                limit=limit,
            )
            return transactions_list, 200

        except Exception as e:
            current_app.logger.info(e)
            print(e)
            transactions_namespace.abort(400, "Operation Error")

    @token_required
    @transactions_namespace.expect(parser, transactions, validate=True)
    @transactions_namespace.marshal_with(transactions, code=201, description="Created")
    @transactions_namespace.response(400, "Operation error")
    @transactions_namespace.response(403, "Input payload validation failed")
    def post(self):
        """Add a transaction for a user"""
        try:
            post_data = request.get_json()
            transaction_owner = TransactionsList.post.owner_id
            transaction_date = post_data.get("transaction_date")
            transaction_type = post_data.get("transaction_type")
            transaction_description = post_data.get("transaction_description")
            transaction_amount = post_data.get("transaction_amount")
            transaction_category_id = post_data.get("transaction_category_id")
            transaction_account_id = post_data.get("transaction_account_id")
            transactions = add_transactions_handler(
                transaction_owner=transaction_owner,
                transaction_date=transaction_date,
                transaction_type=transaction_type,
                transaction_description=transaction_description,
                transaction_amount=transaction_amount,
                transaction_category_id=transaction_category_id,
                transaction_account_id=transaction_account_id,
            )
            return transactions, 201
        except ValidationError:
            transactions_namespace.abort(403, "Input payload validation failed")
        except Exception as e:
            current_app.logger.info(e)
            transactions_namespace.abort(400, "Operation error")


@transactions_namespace.route("/<int:id>", endpoint="transactions")
class Transactions(Resource):
    @token_required
    @transactions_namespace.expect(parser, validate=True)
    @transactions_namespace.marshal_with(transactions, code=200, description="Success")
    @transactions_namespace.response(400, "Operation error")
    @transactions_namespace.response(404, "Transaction <id> does not exists.")
    def get(self, id):
        """Get transaction by id"""
        try:
            user_id = Transactions.get.owner_id
            transaction = get_transactions_by_id(
                id=id,
                transaction_owner=user_id,
            )
            if transaction:
                return transaction, 200
            else:
                raise NotFound
        except NotFound:
            transactions_namespace.abort(404, f"Transaction {id} does not exists.")
        except Exception as e:
            current_app.logger.info(e)
            transactions_namespace.abort(400, "Operation error")

    @token_required
    @transactions_namespace.expect(parser, transactions, validate=True)
    @transactions_namespace.marshal_with(transactions, code=200, description="Success")
    @transactions_namespace.response(400, "Operation error")
    @transactions_namespace.response(403, "Input payload validation failed")
    @transactions_namespace.response(404, "Transaction <id> does not exists.")
    def put(self, id):
        """Update a transaction"""
        try:
            put_data = request.get_json()
            transaction_owner = Transactions.put.owner_id
            transaction_type = put_data.get("transaction_type")
            transaction_date = put_data.get("transaction_date")
            transaction_description = put_data.get("transaction_description")
            transaction_amount = put_data.get("transaction_amount")
            transaction_category_id = put_data.get("transaction_category_id")
            transaction_account_id = put_data.get("transaction_account_id")
            transaction = get_transactions_by_id(
                id=id, transaction_owner=transaction_owner
            )
            if transaction:
                transaction = update_transaction_handler(
                    transaction=transaction,
                    transaction_type=transaction_type,
                    transaction_date=transaction_date,
                    transaction_description=transaction_description,
                    transaction_amount=transaction_amount,
                    transaction_category_id=transaction_category_id,
                    transaction_account_id=transaction_account_id,
                )
                return transaction, 200
            else:
                raise NotFound
        except ValidationError:
            transactions_namespace.abort(403, "Input payload validation failed")
        except NotFound:
            transactions_namespace.abort(404, f"Transaction {id} does not exists.")
        except Exception as e:
            current_app.logger.info(e)
            transactions_namespace.abort(400, "Operation error")

    @token_required
    @transactions_namespace.expect(parser, validate=True)
    @transactions_namespace.response(204, "No Content")
    @transactions_namespace.response(400, "Operation error")
    @transactions_namespace.response(404, "Transaction <id> does not exists.")
    def delete(self, id):
        """Delete a transaction"""
        try:
            user_id = Transactions.delete.owner_id
            transaction = get_transactions_by_id(id=id, transaction_owner=user_id)
            if transaction:
                transaction = delete_transaction_handler(transaction)
                return "", 204
            else:
                raise NotFound
        except NotFound:
            transactions_namespace.abort(404, f"Transaction {id} does not exists.")
        except Exception as e:
            current_app.logger.info(e)
            transactions_namespace.abort(400, "Operation error")
