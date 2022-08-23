from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')

                req = client.post('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': '{}'.format(store.name), 'items': []}, json.loads(req.data))


    def test_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')

                req = client.post('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': '{}'.format(store.name), 'items': []}, json.loads(req.data))

                req = client.post('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 400)
                self.assertDictEqual({'message': "A store with name '{}' already exists.".format(store.name)}, json.loads(req.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')

                req = client.post('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': '{}'.format(store.name), 'items': []}, json.loads(req.data))

                req = client.delete('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(req.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')

                req = client.post('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': '{}'.format(store.name), 'items': []}, json.loads(req.data))

                req2 = client.get('/store/{}'.format(store.name), json={'name': 'test'})

                self.assertEqual(req2.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': '{}'.format(store.name), 'items': []}, json.loads(req2.data))

                

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                req = client.get('/store/test', json={'name': 'test'})

                self.assertEqual(req.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(req.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test').save_to_db()
                item = ItemModel('test_item', 19.99, 1).save_to_db()

                find_req = client.get('/store/test', json={'name': 'test'})

                self.assertEqual(find_req.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}, json.loads(find_req.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test').save_to_db()

                find_req = client.get('/stores')

                self.assertEqual(find_req.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}]}, json.loads(find_req.data))


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                                                
                store = StoreModel('test').save_to_db()
                item = ItemModel('test_item', 19.99, 1).save_to_db()

                find_req = client.get('/stores')

                self.assertEqual(find_req.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}]}]}, json.loads(find_req.data))