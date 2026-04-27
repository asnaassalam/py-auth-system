from validator import Validator
import hashlib 

class User:
    def __init__(self, firstName, lastName, username, password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

    @classmethod
    def from_storage(cls, data):
        user = cls.__new__(cls)
        user._firstName = data.get("firstName", "")
        user._lastName = data.get("lastName", "")
        user._username = data.get("username", "")
        user._password = data.get("password", "")
        return user

    @property
    def firstName(self):
        return self._firstName

    @firstName.setter
    def firstName(self, fname):
        Validator.validateName(fname)
        self._firstName = fname

    @property
    def lastName(self):
        return self._lastName

    @lastName.setter
    def lastName(self, lname):
        Validator.validateName(lname)
        self._lastName = lname

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        Validator.validateUsername(username)
        self._username = username

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, password):
        Validator.validatePassword(password)
        self._password = hashlib.sha256(password.encode()).hexdigest()

    def fullname(self):
        return f"{self._firstName.title()} {self._lastName.title()}" 

    def to_dict(self):
        return {
            "firstName": self._firstName,
            "lastName": self._lastName,
            "username": self._username,
            "password": self._password
        }
        




            

        