from flask_restx import Api

from project.apis.ping import ping_namespace
from project.apis.profiles.views import profile_namespace

api = Api(version="1.0", title="Profile API", doc="/docs")

api.add_namespace(profile_namespace, path="/api/v1/profile-service")
api.add_namespace(ping_namespace, path="/api/v1/profile-service/ping")
