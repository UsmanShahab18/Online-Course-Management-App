from app.models.user_model import User

class UserService:
    def __init__(self, auth_service):
        self.users = auth_service.users # Share users from AuthService for simplicity

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_all_users(self):
        return self.users

    def get_students(self):
        return [user for user in self.users if user.role == "Student"]

    def get_teachers(self):
        return [user for user in self.users if user.role == "Teacher"]

    def update_user_profile(self, user_id, email=None, full_name=None, password=None):
        user = self.get_user_by_id(user_id)
        if user:
            if email: user.email = email
            if full_name: user.full_name = full_name
            if password: user.password = password # In real app, hash password
            print(f"User ID {user_id} profile updated.")
            return True
        print(f"User ID {user_id} not found for profile update.")
        return False
    