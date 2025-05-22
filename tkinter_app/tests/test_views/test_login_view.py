import unittest
import tkinter as tk
from app.views.login_view import LoginView
from app.services.auth_service import AuthService # Import the actual service

class TestLoginView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide the main window for tests
        
        # Mock the callback function
        self.show_main_app_called = False
        def mock_show_main_app(user):
            self.show_main_app_called = True
            self.assertIsNotNone(user, "User object should be passed on successful login")

        self.login_view_frame = LoginView(self.root, mock_show_main_app)
        self.login_view_frame.pack() # Necessary for widgets to be created

    def tearDown(self):
        if self.login_view_frame.winfo_exists():
            self.login_view_frame.destroy()
        if self.root.winfo_exists():
            self.root.destroy()

    def test_login_view_creation(self):
        self.assertIsNotNone(self.login_view_frame)
        self.assertEqual(self.login_view_frame.master.title(), "Login - Online Course Management System")

    def test_login_attempt_successful(self):
        # Use known credentials from AuthService (admin/admin123)
        self.login_view_frame.username_entry.insert(0, "admin")
        self.login_view_frame.password_entry.insert(0, "admin123")
        
        # To avoid messagebox.showinfo/showerror blocking tests, we might need to mock them
        # For simplicity, we'll rely on the callback being called
        
        self.login_view_frame.attempt_login()
        # The actual check is inside mock_show_main_app
        self.assertTrue(self.show_main_app_called, "show_main_app_callback was not called on successful login.")


    def test_login_attempt_failed(self):
        self.login_view_frame.username_entry.insert(0, "wronguser")
        self.login_view_frame.password_entry.insert(0, "wrongpass")
        
        # Mock messagebox.showerror to check if it's called
        original_showerror = tk.messagebox.showerror
        showerror_called_with = None
        def mock_showerror(title, message):
            nonlocal showerror_called_with
            showerror_called_with = (title, message)
        tk.messagebox.showerror = mock_showerror

        self.login_view_frame.attempt_login()
        
        tk.messagebox.showerror = original_showerror # Restore original

        self.assertFalse(self.show_main_app_called, "show_main_app_callback was called on failed login.")
        self.assertIsNotNone(showerror_called_with, "showerror was not called on failed login.")
        self.assertEqual(showerror_called_with[0], "Login Failed")


if __name__ == '__main__':
    unittest.main()