from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                respond = client.post('/store/test')

                self.assertEqual(respond.status_code, 201)

                expected = {'name':'test', 'id':1 ,'items':[]}
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                respond = client.delete('/store/test')

                expected = {'message': 'Store deleted'}

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')

                self.assertIsNotNone(StoreModel.find_by_name('test'))

                respond = client.delete('/store/test')

                expected = {'message': 'Store deleted'}

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                respond = client.get('/store/test')


                expected = {'message': 'Store not found'}

                self.assertEqual(respond.status_code, 404)
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                item = ItemModel('test item', 8.88, 1)

                item.save_to_db()

                respond = client.get('/store/test')

                expected = {'name': 'test', 'id':1 ,'items': [{'name': 'test item', 'price': 8.88}]}
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                store_name = 'test'
                client.post(f'/store/{store_name}')

                respond = client.post(f'/store/{store_name}')

                expected = {'message': f"A store with name '{store_name}' already exists."}

                self.assertEqual(respond.status_code, 400)
                self.assertDictEqual(json.loads(respond.data), expected)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test01')
                client.post('/store/test02')

                respond = client.get('/stores')

                expected = {
                    'stores': [
                    {'name':'test01', 'id':1 ,'items':[]},
                    {'name':'test02', 'id':2 ,'items':[]}
                    ]
                }
                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data), expected)



    def test_store_list_with_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test01')
                client.post('/store/test02')

                item01 = ItemModel('chair', 8.88, 1)
                item02 = ItemModel('desk', 18.88, 2)

                item01.save_to_db()
                item02.save_to_db()

                respond = client.get('/stores')

                expected = {
                    'stores': [
                        {'name': 'test01', 'id':1 ,'items': [{'name':'chair', 'price':8.88}]},
                        {'name': 'test02', 'id':2 ,'items': [{'name':'desk', 'price':18.88}]}
                    ]
                }
                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data), expected)