from models.item import ItemModel


def test_create_item():
    item = ItemModel('test name', 999)
    assert item.name == 'test name'
    assert item.price == 999


def test_item_json():
    item = ItemModel('test name', 999)
    assert item.json() == {'name': 'test name', 'price': 999}
