from tests.base_test import BaseTest
import json
from models.user import UserModel

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username':'test', 'password':'pass'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual(json.loads(request.data), {'message':'User created successfully.'})

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username':'test', 'password':'pass'})

                respond = client.post('/auth',
                                      data=json.dumps({'username':'test', 'password':'pass'}),
                                      headers={'Content-Type':'application/json'})

                self.assertIn('access_token', json.loads(respond.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username':'test', 'password':'pass'})

                respond = client.post('/register', data={'username':'test', 'password':'pass'})

                self.assertEqual(respond.status_code, 400)
                self.assertDictEqual(json.loads(respond.data), {'message':'A user with that name is already exists'})
