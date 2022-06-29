from flask_restx import Namespace, Resource, fields

from project.api.decorator import token_required
from project.api.summary.utils import get_basic_summary

summary_namespace = Namespace("Transactions")

parser = summary_namespace.parser()
parser.add_argument("Authorization", location="headers")

basicSummaryModel = summary_namespace.model(
    "Basic Summary",
    {
        "balance": fields.Float(required=True),
        "incomeMonth": fields.Float(required=True),
        "expenseMonth": fields.Float(required=True),
        "incomeAll": fields.Float(required=True),
        "expenseAll": fields.Float(required=True),
    },
)


@summary_namespace.route("", endpoint="basic-summary")
class BasicSummary(Resource):
    @token_required
    @summary_namespace.expect(parser, validate=True)
    @summary_namespace.marshal_with(basicSummaryModel, code=200, description="success")
    def get(self):
        """Get Basic Summary of the User"""
        try:
            user_id = BasicSummary.get.owner_id
            return get_basic_summary(user_id), 200
        except Exception:
            summary_namespace.abort(400, "Operation Error")
