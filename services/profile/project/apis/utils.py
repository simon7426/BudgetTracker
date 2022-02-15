import jwt
from flask import current_app


def decode_jwt_token(token):
    payload = jwt.decode(
        token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
    )
    return payload
