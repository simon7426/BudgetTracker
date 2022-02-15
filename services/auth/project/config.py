import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "my_precious")
    ACCESS_TOKEN_EXPIRATION = 300
    REFRESH_TOKEN_EXPIRATION = 86400
    ACTIVATION_CODE_EXPIRATION = 1200
    REDIS_URL = os.environ.get("REDIS_URL","redis://localhost:6379/0")
    DEFAULT_ROLE = os.environ.get("DEFAULT_ROLE", "member")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:7426@localhost:5432/flask_auth"
    )
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_TEST_URL", "postgresql://postgres:7426@localhost:5432/flask_auth_test"
    )
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3
    ACTIVATION_CODE_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    url = os.environ.get("DATABASE_URL")

    if url is not None and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    BCRYPT_LOG_ROUNDS = 13
