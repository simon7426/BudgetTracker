from flask import request
from flask_restx import Namespace, Resource, fields

from project.api.decorator import token_required
from project.api.transactions.models import ChoiceType

from project.api.transactions.crud import (  # isort:skip
    add_category,
    get_all_transaction_category,
)

transaction_namespace = Namespace("transaction")

parser = transaction_namespace.parser()
parser.add_argument("Authorization", location="headers")

transaction_category_post = transaction_namespace.model(
    "Transaction Category Post", {"id": fields.Integer(required=True)}
)

transaction_category = transaction_namespace.model(
    "Transaction Category",
    {
        "category_name": fields.String(required=True),
        "category_type": fields.String(
            enum=ChoiceType._member_names_,
            attribute="category_type.value",
            required=True,
        ),
    },
)

# full_transaction_category = transaction_namespace.clone(
#     "Full Transaction Category",
#     transaction_category,
#     {
#         "category_owner": fields.Integer(required=True),
#     }
# )


class Category(Resource):
    @token_required
    @transaction_namespace.marshal_with(
        transaction_category,
        as_list=True,
        code=200,
        description="Fetched all categories.",
    )
    @transaction_namespace.expect(parser)
    @transaction_namespace.response(400, "Object Not Found")
    @transaction_namespace.response(401, "Invalid Token")
    def get(self):
        try:
            categories = get_all_transaction_category(Category.get.owner_id)
            return categories, 200
        except Exception as e:
            print(e)
            return transaction_namespace.abort(400, "Unable to fetch categories.")

    @token_required
    @transaction_namespace.expect(transaction_category, validate=True)
    @transaction_namespace.expect(parser, validate=True)
    @transaction_namespace.marshal_with(transaction_category_post)
    @transaction_namespace.response(201, "Successfully created category <category_id>.")
    @transaction_namespace.response(400, "Operation Error")
    @transaction_namespace.response(401, "Invalid token")
    def post(self):
        try:
            post_data = request.get_json()
            category_name = post_data.get("category_name")
            category_type = post_data.get("category_type")
            category_owner = Category.post.owner_id
            category = add_category(category_name, category_type, category_owner)
            return category, 201
        except Exception as e:
            print(e)
            return transaction_namespace.abort(400, "Unable to create category")


transaction_namespace.add_resource(Category, "/category", endpoint="category")
