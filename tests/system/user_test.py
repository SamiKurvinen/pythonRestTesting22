from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():


                req = client.post('/register', json={'username': 'test', 'password': 'abcd'})

                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(req.data))

    def test_user_login(self):
        with self.app() as client:
            with self.app_context():
                req = client.post('/register', json={'username': 'test', 'password': 'abcd'})
                auth_req = client.post('/auth',
                                        data=json.dumps({'username': 'test', 'password': 'abcd'}),
                                        headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_req.data).keys())

    def test_user_exists(self):
        with self.app() as client:
            with self.app_context():


                req = client.post('/register', json={'username': 'test', 'password': 'abcd'})

                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(req.data))

                req = client.post('/register', json={'username': 'test', 'password': 'abcd'})

                self.assertEqual(req.status_code, 400)
                
                self.assertDictEqual({'message': 'Username already in use'}, json.loads(req.data))