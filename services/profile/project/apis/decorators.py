from functools import wraps

import jwt
from flask import abort, request

from project.apis.utils import decode_jwt_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            abort(401, "Invalid Token")
        try:
            access_token = auth_header.split(" ")[-1]
            payload = decode_jwt_token(access_token)
            if (
                "sub" not in payload
                or "role" not in payload
                or "type" not in payload
                or payload["type"] != "access"
            ):
                abort(401, "Invalid Token")
            setattr(decorated, "owner_id", payload["sub"])
            setattr(decorated, "owner_role", payload["role"])
        except jwt.ExpiredSignatureError:
            abort(401, "Token Expired")
        except jwt.InvalidTokenError:
            abort(401, "Invalid Token")

        return f(*args, **kwargs)

    return decorated
