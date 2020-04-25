from models.store import StoreModel
from models.item import ItemModel


def test_create_store_items_empty():
    store = StoreModel('test_store')

    assert store.items.all() == [], \
        "The store's items length is not 0 even though any item was not added"


def test_crud(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        store = StoreModel('test_store')
        assert StoreModel.find_by_name('test_store') is None, "Store Table is not empty after creating"
        store.save_to_db()
        assert StoreModel.find_by_name('test_store') is not None, "Store Table is empty after adding object"
        store.delete_from_db()
        assert StoreModel.find_by_name('test_store') is None, "Store Table is not empty after deleting object"


def test_store_relationship(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        store = StoreModel('test_store')
        item = ItemModel('test_item', 99.9, 1)
        store.save_to_db()
        item.save_to_db()

        assert store.items.count() == 1
        assert store.items.first().name == 'test_item'


def test_store_json_without_items():
    store = StoreModel('test_store')
    expected = {'id': None, 'name': 'test_store', 'items': []}
    assert store.json() == expected, "json method returns incorrect data with empty store"


def test_store_json_with_item(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        store = StoreModel('test_store')
        item = ItemModel('test_item', 99.9, 1)
        store.save_to_db()
        item.save_to_db()
        expected = {'id': 1, 'name': 'test_store', 'items': [{'name': 'test_item', 'price': 99.9}]}
        assert store.json() == expected, "json method returns incorrect data with one item in the store"
