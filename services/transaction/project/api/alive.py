from flask_restx import Namespace, Resource, fields

alive_namespace = Namespace("Alive")

response = alive_namespace.model(
    "Alive",
    {
        "message": fields.String(required=True),
    },
)


class Alive(Resource):
    @alive_namespace.marshal_with(response)
    @alive_namespace.response(200, "Alive")
    def get(self):
        response = {"message": "Alive"}
        return response, 200


alive_namespace.add_resource(Alive, "", endpoint="alive")
