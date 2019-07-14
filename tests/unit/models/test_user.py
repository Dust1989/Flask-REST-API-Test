from tests.unit.unit_base_test import UnitBaseTest

from models.user import UserModel

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('user', 'pass')

        self.assertEqual(user.username, 'user')
        self.assertEqual(user.password, 'pass')