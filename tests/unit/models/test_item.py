from models.item import ItemModel


def test_create_item():
    item = ItemModel('test name', 999, 1)
    assert item.name == 'test name', "The name of the item after creation does not equal the constructor argument"
    assert item.price == 999, "The price of the item after creation does not equal the constructor argument"
    assert item.store_id == 1, "The store_id of the item after creation does not equal the constructor argument"
    assert item.store is None, "The store is created that is not correct"


def test_item_json():
    item = ItemModel('test name', 999, 1)
    assert item.json() == {'name': 'test name', 'price': 999}
