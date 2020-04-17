from models.store import StoreModel


def test_create_store():
    store = StoreModel('test_store')

    assert store.name == 'test_store', "The name of the item after creation does not equal the constructor argument"
