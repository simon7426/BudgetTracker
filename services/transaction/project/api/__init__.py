from flask_restx import Api

from project.api.alive import alive_namespace
from project.api.transaction_categories.views import transaction_category_namespace

api = Api(version="1.0", title="Budget Tracker Transaction Service API", doc="/docs")

api.add_namespace(alive_namespace, path="/api/v1/transactions-service/alive")
api.add_namespace(transaction_category_namespace, path="/api/v1/transactions-service/category")
