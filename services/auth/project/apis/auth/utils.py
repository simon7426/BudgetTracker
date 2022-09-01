import requests
from flask import current_app

from project import redis_client


def add_token_to_blacklist(token):
    return redis_client.set(
        token, "1", ex=current_app.config.get("REFRESH_TOKEN_EXPIRATION")
    )


def check_token_in_blacklist(token):
    if redis_client.get(token):
        return True
    else:
        return False


def verify_recaptcha(token, action):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": current_app.config["RECAPTCHA_SERVER_KEY"], "response": token}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url=url, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["success"] and data["action"] == action and data["score"] > 0.5:
            return True

    return False
