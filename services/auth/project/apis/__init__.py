from flask_restx import Api

from project.apis.auth.auth import auth_namespace
from project.apis.ping.api import ping_namespace

api = Api(version="1.0", title="Users API", doc="/docs")

api.add_namespace(ping_namespace, path="/api/v1/auth-service/ping")
api.add_namespace(auth_namespace, path="/api/v1/auth-service")
