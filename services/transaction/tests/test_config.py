import os


def test_development_config(test_app):
    test_app.config.from_object("project.config.DevelopmentConfig")
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert not test_app.config["TESTING"]
    assert not test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert test_app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")
    assert not test_app.config["RESTX_ERROR_404_HELP"]


def test_testing_config(test_app):
    test_app.config.from_object("project.config.TestingConfig")
    assert test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )
    assert not test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert test_app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")
    assert not test_app.config["RESTX_ERROR_404_HELP"]
    assert not test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]


def test_production_config(test_app):
    test_app.config.from_object("project.config.ProductionConfig")
    assert test_app.config["SECRET_KEY"] == os.getenv("SECRET_KEY", "my_precious")
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["RESTX_ERROR_404_HELP"]
    assert not test_app.config["TESTING"]
    assert not test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]
