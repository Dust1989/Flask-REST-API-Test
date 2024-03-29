from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel

class StoreTest(BaseTest):

    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Found an store with name {}, but expected not to.".format(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))


    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, item.name)

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name':'test store',
                'id':1,
                'items':[
                    {'name':'test',
                          'price': 19.99
                     }
                         ]
            }
            self.assertDictEqual(store.json(), expected)
