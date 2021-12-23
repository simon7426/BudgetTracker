from flask_restx import Api

from project.api.alive import alive_namespace
from project.api.transactions.apis import transaction_namespace

api = Api(version="1.0", title="Budget Tracker Transaction Service API", doc="/docs")

api.add_namespace(alive_namespace, path="/alive")
api.add_namespace(transaction_namespace, path="/api/v1/transactions")
