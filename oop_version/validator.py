import re

class Validator:
    def validateName(name):
        name = name.strip()
        if not name:
            raise ValueError("Name can not be empty.")
        elif not re.match(r'^[A-Za-z]{2,30}$', name):
            raise ValueError("Name can only contain letters and must be between 2 and 30 characters.")
        else:
            return None

    def validateUsername(username):
        if not username:
            raise ValueError("Username can not be empty.")
        elif username != username.strip():
            raise ValueError("Username can not start or end with whitespace.")
        elif len(username) < 4:
            raise ValueError("Username must be atleast 4 characters.")
        elif re.search(r'\s', username):
            raise ValueError("Username can not contain whitespaces.")
        elif not re.match(r'^[a-z0-9_]+$', username):  
            raise ValueError("Username can only contain lower case letters, numbers and underscores(_)")
        else:
            return None

    def validatePassword(password):
        if not password:
            raise ValueError("Password can not be empty.")
        elif password != password.strip():
            raise ValueError("Password can not start or end with whitespace.")
        elif re.search(r'\s', password):
            raise ValueError("Password can not contain whitespaces.")
        elif len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        elif not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter.")
        elif not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
        elif not re.search(r'\d', password):
            raise ValueError("Password must contain at least one digit.")
        elif not re.search(r'[@$!%*?&#_]', password):
            raise ValueError("Password must contain at least one special character (@$!%*?&#_).")
        else:
            return None            