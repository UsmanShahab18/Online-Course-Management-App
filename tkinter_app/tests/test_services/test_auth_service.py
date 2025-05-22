import unittest
from app.services.auth_service import AuthService
from app.models.user_model import User

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService()
        # Reset users for predictable tests if AuthService modifies its internal list
        self.auth_service.users = [
            User(1, "admin", "admin123", "Admin", "admin@example.com", "Admin User"),
            User(2, "teacher1", "teacher123", "Teacher", "teacher1@example.com", "Prof. Ada"),
            User(3, "student1", "student123", "Student", "student1@example.com", "John Doe")
        ]
        self.auth_service.current_user = None


    def test_login_successful(self):
        user = self.auth_service.login("admin", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.role, "Admin")
        self.assertEqual(self.auth_service.get_current_user(), user)

    def test_login_failed_wrong_username(self):
        user = self.auth_service.login("wronguser", "admin123")
        self.assertIsNone(user)
        self.assertIsNone(self.auth_service.get_current_user())

    def test_login_failed_wrong_password(self):
        user = self.auth_service.login("admin", "wrongpass")
        self.assertIsNone(user)
        self.assertIsNone(self.auth_service.get_current_user())

    def test_logout(self):
        self.auth_service.login("student1", "student123")
        self.assertIsNotNone(self.auth_service.get_current_user())
        self.auth_service.logout()
        self.assertIsNone(self.auth_service.get_current_user())

    def test_get_current_user_initially_none(self):
        self.assertIsNone(self.auth_service.get_current_user())

    def test_register_user(self):
        initial_user_count = len(self.auth_service.users)
        new_user = self.auth_service.register_user("newbie", "newpass", "Student", "new@example.com", "New B. User")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, "newbie")
        self.assertEqual(len(self.auth_service.users), initial_user_count + 1)
        
        # Check if the new user can login
        logged_in_new_user = self.auth_service.login("newbie", "newpass")
        self.assertEqual(logged_in_new_user, new_user)

if __name__ == '__main__':
    unittest.main()