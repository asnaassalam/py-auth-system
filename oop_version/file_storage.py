import hashlib
import json
from pathlib import Path
from user import User


class FileStorage:
    def __init__(self):
        self.data_file = Path(__file__).with_name("users.json")
        self.user_details = self.load_users()

    def next_user_id(self):
        current_ids = []
        for user_detail in self.user_details.values():
            if isinstance(user_detail, dict):
                try:
                    current_ids.append(int(user_detail.get("Id", 0)))
                except (TypeError, ValueError):
                    continue
        return max(current_ids, default=0) + 1

    def load_users(self):
        if not self.data_file.exists():
            return {}

        with self.data_file.open("r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return {}

            try:
                user_details = json.loads(content)
            except json.JSONDecodeError:
                return {}

        return user_details if isinstance(user_details, dict) else {}

    def save_users(self):
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(self.user_details, file, indent=2)
            

    def save_user(self, user):
        detail = user.to_dict()
        username = detail.get("username")
        if not username:
            return "Invalid user details"

        user_detail = {
            "Id": self.next_user_id(),
            "firstName": detail.get("firstName"),
            "lastName": detail.get("lastName"),
            "username": detail.get("username"),
            "password": detail.get("password")
        }
        self.user_details[username] = user_detail
        self.save_users()
        return "User saved successfully"

    def check_user(self, username, password):
        user_detail = self.user_details.get(username)
        if not user_detail:
            return "User not found", None

        if user_detail.get("password") == hashlib.sha256(password.encode()).hexdigest():
            return "User found", User.from_storage(user_detail)
        else:
            return "Incorrect password", None


    def check_username_exists(self, username):
        return username in self.user_details
