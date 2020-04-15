import pytest
from app import app
from db import db


@pytest.fixture(scope="function")
def tc_app_db_env():
    # Make sure Database exists
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    with app.app_context():
        db.init_app(app)
        db.create_all()
    # Get a test client
    tc_app = app.test_client()
    tc_app_context = app.app_context
    yield tc_app_context
    # Cleaning Database after test
    with app.app_context():
        db.session.remove()
        db.drop_all()
