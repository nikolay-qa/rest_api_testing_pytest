from models.store import StoreModel
from models.item import ItemModel
import json


def test_create_store(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            response = client.post('/store/test_store')
            assert response.status_code == 201
            assert json.loads(response.data) == {'name': 'test_store', 'items': []}
            assert StoreModel.find_by_name('test_store') is not None


def test_create_duplicate_store(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            client.post('/store/test_store')
            response = client.post('/store/test_store')
            assert response.status_code == 400
            assert json.loads(response.data) == {'message': "A store with name 'test_store' already exists."}


def test_delete_store(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            client.post('/store/test_store')
            response = client.delete('/store/test_store')
            assert response.status_code == 200
            assert json.loads(response.data) == {'message': 'Store deleted'}
            assert StoreModel.find_by_name('test_store') is None


def test_find_store(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            client.post('/store/test_store')
            response = client.get('/store/test_store')
            assert json.loads(response.data) == {'name': 'test_store', 'items': []}
            assert response.status_code == 200


def test_store_not_found(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            response = client.get('/store/test_store')
            assert StoreModel.find_by_name('test_store') is None
            assert response.status_code == 404
            assert json.loads(response.data) == {'message': 'Store not found'}


def test_store_found_with_items(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store').save_to_db()
            ItemModel('test_item', 99.9, 1).save_to_db()
            response = client.get('/store/test_store')
            assert json.loads(response.data) == {'name': 'test_store', 'items': [{'name': 'test_item', 'price': 99.9}]}
            assert response.status_code == 200


def test_store_list(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            StoreModel('test_store_2').save_to_db()
            response = client.get('/stores')
            assert response.status_code == 200
            assert json.loads(response.data) == \
                   {'stores': [{'name': 'test_store_1', 'items': []}, {'name': 'test_store_2', 'items': []}]}


def test_store_list_with_items(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app() as client:
        with tc_app_context():
            StoreModel('test_store_1').save_to_db()
            StoreModel('test_store_2').save_to_db()
            ItemModel('test_item_1', 11.1, 1).save_to_db()
            ItemModel('test_item_2', 2.2, 2).save_to_db()
            response = client.get('/stores')
            assert response.status_code == 200
            assert json.loads(response.data) == \
                   {'stores': [{'name': 'test_store_1', 'items': [{'name': 'test_item_1', 'price': 11.1}]},
                               {'name': 'test_store_2', 'items': [{'name': 'test_item_2', 'price': 2.2}]}]}
