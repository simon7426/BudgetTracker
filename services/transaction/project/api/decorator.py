from functools import wraps

from flask import abort, request

from project.api.utils import decode_jwt_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            abort(401, "Invalid token")
        try:
            access_token = auth_header.split(" ")[-1]
            payload = decode_jwt_token(access_token)
            if not payload:
                abort(401, "Invalid Token")
            setattr(decorated, "owner_id", payload["sub"])
            setattr(decorated, "owner_role", payload["role"])
        except Exception as e:
            print(e)
            abort(401, "Invalid Token")
        return f(*args, **kwargs)

    return decorated
