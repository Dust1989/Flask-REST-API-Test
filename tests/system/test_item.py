from tests.base_test import BaseTest
from models.item import ItemModel
import json
from models.user import UserModel


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()

        with self.app() as client:
            with self.app_context():
                UserModel('test', 'pass').save_to_db()
                token_respond = client.post('/auth',
                                            data=json.dumps({'username':'test', 'password':'pass'}),
                                            headers={'Content-Type':'application/json'})

                self.token = json.loads(token_respond.data)['access_token']



    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                respond = client.get('/item/test')

                expected = {'message':'Could not authorize. Did you include a valid Authorization header?'}

                self.assertEqual(respond.status_code, 401)
                self.assertEqual(json.loads(respond.data), expected)


    # need to be authenticate
    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                respond = client.get('/item/test',headers={'Authorization':f'jwt {self.token}'})

                self.assertEqual(respond.status_code, 404)
                self.assertEqual(json.loads(respond.data), {'message': 'Item not found'})


    # need to be authenticate
    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                item = ItemModel('test', 8.88, 1)
                item.save_to_db()

                respond = client.get('/item/test',
                                     headers={'Authorization': f'jwt {self.token}'})

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data), {'name':'test', 'price':8.88})


    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                item = ItemModel('test', 8.88, 1)
                item.save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('test'))

                respond = client.delete('/item/test')

                self.assertIsNone(ItemModel.find_by_name('test'))

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data),
                                 {'message': 'Item deleted'})


    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                respond = client.post('/item/test',
                                      data=json.dumps({'price':8.88, 'store_id': 1}),
                                      headers={'Content-Type': 'application/json'})

                self.assertEqual(respond.status_code, 201)
                self.assertEqual(json.loads(respond.data),
                                 {'name': 'test', 'price':8.88})
                self.assertIsNotNone(ItemModel.find_by_name('test'))


    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                item = ItemModel('test', 8.88, 1)
                item.save_to_db()

                respond = client.post('/item/test',
                                      data=json.dumps({'price': 8.88, 'store_id': 1}),
                                      headers={'Content-Type': 'application/json'})

                self.assertEqual(respond.status_code, 400)
                self.assertEqual(json.loads(respond.data),
                                 {'message': "An item with name '{}' already exists.".format(item.name)})


    def test_put_item(self):
        with self.app() as client:
            with self.app_context():

                respond = client.put('/item/test',
                                      data=json.dumps({'price': 8.88, 'store_id': 1}),
                                      headers={'Content-Type': 'application/json'})

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data),{'name':'test', 'price':8.88})


    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                item = ItemModel('test', 8.88, 1)
                item.save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 8.88)

                respond = client.put('/item/test',
                                     data=json.dumps({'price': 9.99, 'store_id': 1}),
                                     headers={'Content-Type': 'application/json'})

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data),
                                 {'name': 'test', 'price': 9.99})


    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                respond = client.get('/items')

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data),
                                 {'items': []})

                item = ItemModel('test', 8.88, 1)
                item.save_to_db()

                respond = client.get('/items')

                self.assertEqual(respond.status_code, 200)
                self.assertEqual(json.loads(respond.data),
                                 {'items':[{'name': 'test', 'price': 8.88}]})




