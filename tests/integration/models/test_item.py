from models.item import ItemModel
from models.store import StoreModel


def test_crud(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        StoreModel('test').save_to_db()
        item = ItemModel('test name', 99.9, 1)
        assert ItemModel.find_by_name('test name') is None, \
            f"Found an item with name '{item.name}', but expected not to"
        item.save_to_db()
        assert ItemModel.find_by_name('test name') is not None, \
            f"Item '{item.name}' was not added to the database"
        item.delete_from_db()
        assert ItemModel.find_by_name('test name') is None, \
            f"Item '{item.name}' was not deleted from the database"


def test_store_relationship(tc_app_db_env):
    tc_app, tc_app_context = tc_app_db_env
    with tc_app_context():
        store = StoreModel('test_store')
        item = ItemModel('test', 99.9, 1)

        store.save_to_db()
        item.save_to_db()

        assert item.store.name == 'test_store'
