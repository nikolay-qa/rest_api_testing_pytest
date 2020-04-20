from models.user import UserModel
import json


def test_register_user(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            response = client.post('/register', data={'username': 'test_user', 'password': 'qwerty'})

            assert json.loads(response.data) == {'message': 'User created successfully.'}
            assert response.status_code == 201
            assert UserModel.find_by_username('test_user')


def test_register_and_login(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            client.post('/register', data={'username': 'test_user', 'password': 'qwerty'})
            auth_response = client.post('/auth',
                                       data=json.dumps({'username': 'test_user', 'password': 'qwerty'}),
                                       headers={'Content-Type': 'application/json'})

            assert 'access_token' in json.loads(auth_response.data).keys()   # ['access_token']


def test_register_duplicate_user(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            client.post('/register', data={'username': 'test_user', 'password': 'qwerty'})
            response = client.post('/register', data={'username': 'test_user', 'password': 'qwerty'})
            assert response.status_code == 400
            assert json.loads(response.data) == {'message': 'A user with that username already exist'}
