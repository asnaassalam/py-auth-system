from user import User
from file_storage import FileStorage

storage = FileStorage()

class AuthManager:
    def register(fname, lname, username, password):
        try:
            user = User(fname, lname, username, password)
            if storage.check_username_exists(username):
                return "error", "Username already exists"
        except ValueError as e:
            return "error", str(e)
        else:
            storage.save_user(user)
            return "success", "User registered successfully"

    def login(username, password):  
        status, user = storage.check_user(username, password)
        return status, user
        

