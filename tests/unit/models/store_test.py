from models.store import StoreModel
from tests.unit.unit_base_test import UnitBase

class StoreTest(UnitBase):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test')