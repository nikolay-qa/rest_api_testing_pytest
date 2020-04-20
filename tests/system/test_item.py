from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
import json


def test_get_item_no_auth_token(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            response = client.get('/item/test_item_1')
            assert response.status_code == 401
            assert json.loads(response.data) == \
                   {'message': 'Could not authorize. Did you include a valid Authorization header?'}


def test_get_item_not_found(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            UserModel('test_user', 'qwerty').save_to_db()
            auth_response = client.post('/auth',
                                        data=json.dumps({'username': 'test_user', 'password': 'qwerty'}),
                                        headers={'Content-Type': 'application/json'})
            auth_token = json.loads(auth_response.data)['access_token']
            header = {'Authorization': f"JWT {auth_token}"}
            response = client.get('/item/wrong_item', headers=header)
            assert response.status_code == 404
            assert json.loads(response.data) == {'message': 'Item not found'}


def test_get_existed_item_with_auth_token(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            UserModel('test_user', 'qwerty').save_to_db()
            StoreModel('test_store_1').save_to_db()
            ItemModel('test_item_1', 99.9, 1).save_to_db()
            auth_response = client.post('/auth',
                                        data=json.dumps({'username': 'test_user', 'password': 'qwerty'}),
                                        headers={'Content-Type': 'application/json'})
            auth_token = json.loads(auth_response.data)['access_token']
            header = {'Authorization': f"JWT {auth_token}"}
            response = client.get('/item/test_item_1', headers=header)
            assert response.status_code == 200
            assert json.loads(response.data) == {'name': 'test_item_1', 'price': 99.9}


def test_delete_existed_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            ItemModel('test_item_1', 99.9, 1).save_to_db()
            response = client.delete('/item/test_item_1')
            assert response.status_code == 200
            assert json.loads(response.data) == {'message': 'Item deleted'}


def test_create_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            response = client.post('/item/test_item_1',
                                   data={'price': 99.9, 'store_id': 1})
            assert response.status_code == 201
            assert json.loads(response.data) == {'name': 'test_item_1', 'price': 99.9}


def test_create_duplicate_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            client.post('/item/test_item_1', data={'price': 99.9, 'store_id': 1})
            response = client.post('/item/test_item_1', data={'price': 99.9, 'store_id': 1})
            assert response.status_code == 400
            assert json.loads(response.data) == {'message': "An item with name 'test_item_1' already exists."}


def test_put_update_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            ItemModel('test_item_1', 99.9, 1).save_to_db()
            response = client.put('/item/test_item_1', data={'price': 33.3, 'store_id': 1})
            assert response.status_code == 200
            assert json.loads(response.data) == {'name': 'test_item_1', 'price': 33.3}


def test_put_create_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            response = client.put('/item/test_item_1', data={'price': 33.3, 'store_id': 1})
            assert response.status_code == 200
            assert json.loads(response.data) == {'name': 'test_item_1', 'price': 33.3}


def test_get_item_list(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            StoreModel('test_store_1').save_to_db()
            ItemModel('test_item_1', 10.9, 1).save_to_db()
            ItemModel('test_item_2', 22.2, 2).save_to_db()
            ItemModel('test_item_3', 562.9, 1).save_to_db()
            response = client.get('/items')
            assert response.status_code == 200
            assert json.loads(response.data) == {'items': [{'name': 'test_item_1', 'price': 10.9},
                                                           {'name': 'test_item_2', 'price': 22.2},
                                                           {'name': 'test_item_3', 'price': 562.9}]}
