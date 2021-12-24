from datetime import datetime, timedelta

import jwt
from flask import current_app


def get_bd_time():
    return datetime.utcnow() + timedelta(hours=6)


def decode_jwt_token(token):
    payload = jwt.decode(
        token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
    )
    return payload


def generate_token_for_test(user_id, role, token_type, exp, secret):
    payload = {"sub": user_id, "role": role, "type": token_type, "exp": exp}
    encoded_token = jwt.encode(payload, secret, algorithm="HS256")
    return encoded_token
