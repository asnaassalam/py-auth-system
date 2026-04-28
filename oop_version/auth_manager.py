from user import User
from file_storage import FileStorage
import hashlib

class AuthManager:
    storage = FileStorage()

    @staticmethod
    def register(fname, lname, username, password):
        try:
            user = User(fname, lname, username, password)
            if AuthManager.storage.check_username_exists(username):
                return "error", "Username already exists"
        except ValueError as e:
            return "error", str(e)
        else:
            AuthManager.storage.save_user(user)
            return "success", "User registered successfully"

    @staticmethod
    def login(username, password):  
        user_detail = AuthManager.storage.check_user(username, password)
        if not user_detail:
            return "error", "User not found"
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if user_detail.get("password") == hashed:
            return "User found", User.from_storage(user_detail)
        else:
            return "error", None
        

