from models.user import UserModel
from tests.unit.unit_base_test import UnitBase

class UserTest(UnitBase):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')