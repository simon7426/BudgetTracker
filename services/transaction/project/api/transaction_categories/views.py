from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

from project.api.decorator import token_required
from project.api.models import ChoiceType

from project.api.transaction_categories.crud import (  # isort:skip
    add_category,
    delete_category,
    get_all_transaction_category,
    get_transaction_category,
    update_category,
)


transaction_category_namespace = Namespace("transaction-categories")

parser = transaction_category_namespace.parser()
parser.add_argument("Authorization", location="headers")

transaction_category = transaction_category_namespace.model(
    "Transaction Category",
    {
        "id": fields.Integer(readOnly=True, description="Category Identifier"),
        "category_name": fields.String(required=True, description="Category Name"),
        "category_type": fields.String(
            enum=ChoiceType._member_names_,
            attribute="category_type.value",
            required=True,
            description="Category Type",
        ),
    },
)

class CategoryList(Resource):
    @token_required
    @transaction_category_namespace.marshal_with(
        transaction_category,
        as_list=True,
        code=200,
        description="Fetched all categories.",
    )
    @transaction_category_namespace.expect(parser)
    @transaction_category_namespace.response(400, "Object Not Found")
    @transaction_category_namespace.response(401, "Invalid Token")
    def get(self):
        try:
            categories = get_all_transaction_category(CategoryList.get.owner_id)
            return categories, 200
        except Exception as e:
            print(e)
            return transaction_category_namespace.abort(400, "Unable to fetch categories.")

    @token_required
    @transaction_category_namespace.expect(transaction_category, validate=True)
    @transaction_category_namespace.expect(parser, validate=True)
    @transaction_category_namespace.marshal_with(transaction_category)
    @transaction_category_namespace.response(201, "Successfully created category <category_id>.")
    @transaction_category_namespace.response(401, "Invalid token")
    @transaction_category_namespace.response(400, "Operation Error")
    def post(self):
        try:
            post_data = request.get_json()
            category_name = post_data.get("category_name")
            category_type = post_data.get("category_type")
            category_owner = CategoryList.post.owner_id
            category = add_category(category_name, category_type, category_owner)
            return category, 201
        except Exception as e:
            print(e)
            return transaction_category_namespace.abort(400, "Unable to create category")


class Category(Resource):
    @token_required
    @transaction_category_namespace.expect(parser, validate=True)
    @transaction_category_namespace.marshal_with(transaction_category)
    @transaction_category_namespace.response(200, "successfully retrived category")
    @transaction_category_namespace.response(400, "Operation Error")
    @transaction_category_namespace.response(401, "Invalid Token")
    @transaction_category_namespace.response(404, "No Such Category")
    def get(self, id):
        try:
            category = get_transaction_category(id, Category.get.owner_id)
            if category:
                return category, 200
            else:
                transaction_category_namespace.abort(404, "No Such Category")

        except NotFound as e:
            print(e)
            transaction_category_namespace.abort(404, "No Such Category")

        except Exception as e:
            print(e)
            transaction_category_namespace.abort(400, "Operation Error")

    @token_required
    @transaction_category_namespace.expect(transaction_category, validate=True)
    @transaction_category_namespace.expect(parser, validate=True)
    @transaction_category_namespace.marshal_with(transaction_category)
    @transaction_category_namespace.response(200, "Successfully updated category")
    @transaction_category_namespace.response(400, "Operation Error")
    @transaction_category_namespace.response(401, "Invalid Token")
    @transaction_category_namespace.response(404, "No Such Category")
    def put(self, id):
        try:
            put_data = request.get_json()
            category_name = put_data.get("category_name")
            category_type = put_data.get("category_type")
            category = get_transaction_category(id, Category.put.owner_id)
            if category:
                updated_category = update_category(
                    category, category_name, category_type
                )
                return updated_category, 200
            else:
                transaction_category_namespace.abort(404, "No Such Category")

        except NotFound as e:
            print(e)
            transaction_category_namespace.abort(404, "No Such Category")

        except Exception as e:
            print(e)
            transaction_category_namespace.abort(400, "Operation Error")

    @token_required
    @transaction_category_namespace.expect(parser, validate=True)
    @transaction_category_namespace.response(204, "")
    @transaction_category_namespace.response(400, "Operation Error")
    @transaction_category_namespace.response(401, "Invalid Token")
    @transaction_category_namespace.response(404, "No Such Category")
    def delete(self, id):
        try:
            category = get_transaction_category(id, Category.delete.owner_id)
            if category:
                delete_category(category)
                return "", 204
            else:
                transaction_category_namespace.abort(404, "No Such Category.")
        except NotFound as e:
            print(e)
            transaction_category_namespace.abort(404, "No Such Category")
        except Exception as e:
            print(e)
            transaction_category_namespace.abort(400, "Operation Error")


transaction_category_namespace.add_resource(CategoryList, "", endpoint="category-list")
transaction_category_namespace.add_resource(Category, "/<int:id>", endpoint="category")
