from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
from resources.item import ItemList
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': 'abcd'})
                auth_req = client.post('/auth',
                                        data=json.dumps({'username': 'test', 'password': 'abcd'}),
                                        headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_req.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(json.loads(resp.data), {'name': 'test', 'price': 19.99})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_create_item_duplicate(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                resp = client.post('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))
                resp = client.put('/item/test', json={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_list_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

                list = client.get('/items')
                self.assertEqual(list.status_code, 200)
                self.assertDictEqual({'items' :[{'name': 'test', 'price': 19.99}]}, json.loads(list.data))