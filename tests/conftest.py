import pytest
from app import app
from db import db


@pytest.fixture(scope="session")
def init_app():
    # Make sure Database exists
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    with app.app_context():
        db.init_app(app)
    yield app


@pytest.yield_fixture(scope="function")
def tc_app_db_env(init_app):
    with init_app.app_context():
        db.create_all()
    # Testing begin here
        yield init_app.test_client, init_app.app_context
    # Cleaning Database after test
    with init_app.app_context():
        db.session.remove()
        db.drop_all()
