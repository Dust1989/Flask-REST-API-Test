from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest



class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test store')

        self.assertEqual(store.name, 'test store',
                         "The name of the store after creation does not equal the constructor argument.")

    def test_store_json(self):
        store = StoreModel('test store')
        expected = {
            'name': 'test store',
            'items': []
        }

        self.assertEqual(
            store.json(),
            expected,
            "The JSON export of the store is incorrect. Received {}, expected {}.".format(
                store.json(), expected))
