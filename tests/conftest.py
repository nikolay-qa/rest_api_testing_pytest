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
    # Getting a test client
    yield app.test_client, app.app_context
    # Cleaning Database after test
    with app.app_context():
        db.session.remove()
        db.drop_all()
