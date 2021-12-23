from datetime import datetime, timedelta

import jwt
from flask import current_app


def get_bd_time():
    return datetime.utcnow() + timedelta(hours=6)


def decode_jwt_token(token):
    payload = jwt.decode(
        token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
    )
    if payload["type"] == "access":
        return payload
    return None
