class User:
    def __init__(self, user_id, username, password, role, email="", full_name=""):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role # Admin, Teacher, Student
        self.email = email
        self.full_name = full_name

    def __str__(self):
        return f"User(ID: {self.user_id}, Username: {self.username}, Role: {self.role})"