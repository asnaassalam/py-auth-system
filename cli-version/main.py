# Import json module
import json
# Import hashlib module for password hashing using SHA-256
import hashlib
# Import re module for regular expression operations
import re

# Function to display a styled message box
def display_message(user_text):
    box_width = 36
    text = user_text
    padding = (box_width - len(text) - 2) // 2
    print("=" * box_width)
    print("|" + " " * padding + text + " " * (box_width - len(text) - padding - 2) + "|")
    print("=" * box_width)

# Takes a plain text password, encodes it, and returns the hexadecimal hash
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Try to load existing user details from a JSON file
try:
    with open("users.json", "r") as file1:
        user_details = json.load(file1)
except FileNotFoundError:
    user_details = {}

# Function to validate username
def validateUsername(username, user_details=user_details):
    if not username:
        return "Username cannot be empty."
    elif username in user_details:
        return "User already exists. Please enter another username."     
    elif len(username) < 8:
        return "Username must be less than 8 characters."
    elif " " in username:
        return "Username cannot contain spaces."
    elif not re.match(r'^[a-z0-9_]+$', username):
        return "Username can only contain simple letters, numbers and underscores."
    return None  

# Function to validate password
def validatePassword(password):
    if not password:
        return "Password cannot be empty."  
    elif len(password) < 6:
        return "Password must be at least 6 characters long."
    elif not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    elif not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    elif not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None      
       
# Registration function
def registration():
    print("\n")
    display_message("Register Here!")
    while True:
        username = input("Username: ").strip()
        username_error = validateUsername(username)
        if username_error:
            print(f"\033[31m{username_error}\033[0m")
            continue
        while True:
            password = input("Password: ").strip()
            password_error = validatePassword(password)
            if password_error:
                print(f"\033[31m{password_error}\033[0m")
                continue             
            else:
                user_details[username] = hash_password(password)
                with open("users.json", "w") as file2:
                    json.dump(user_details, file2, indent=4)
                    print("\033[32mRegistration Successful!\n\033[0m")
                return

# Password change function
def change_password(username):
    print("\n")
    display_message("Change Password")
    old_password = input("Old Password: ").strip()
    if user_details[username] == hash_password(old_password):
        new_password = input("New Password: ")
        password_error = validatePassword(new_password)
        if password_error:
            print(f"\033[31m{password_error}\033[0m")
        else:
            user_details[username] = hash_password(new_password)
            print("\033[32mPassword changed Successfully.\033[0m")
    else:
        print("\033[31mIncorrect Password. Please try again.\n\033[0m")

# Login function
def login():
    print("\n")
    display_message("Enter your credentials to Login!")
    counter = 1
    while counter < 4:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username in user_details:
            if user_details[username] == hash_password(password):
                print("\n")
                display_message("Welcome, Login Successful!")
                while True:
                    print("\n--- Menu ---")
                    print("1. View Profile")
                    print("2. Change password")
                    print("3. Logout")
                    try:
                        menu = int(input("Enter 1/2/3: "))
                    except ValueError:
                        print("\033[31mInvalid input.\n\033[0m")
                        continue
                    match menu:
                        case 1:
                            print("\n")
                            display_message("Profile Details")
                            print(f"Username: {username}")
                            i = 1
                            print("Password: ", sep="", end="")
                            while i < len(user_details[username]) - 1:
                                print("*", sep="", end="")
                                i = i + 1
                            print(user_details[username][-2:])
                        case 2:
                            change_password(username)
                        case 3:
                            print("\033[32mYou have been logged out successfully.\n\033[0m")
                            break
                        case _:
                            print("\033[31mInvalid option.\n\033[0m")
                break
            else:
                print(f"\033[31mIncorrect password. {3 - counter} attempt(s) left.\n\033[0m")
        else:
            if counter < 3:
                print(f"\033[31mUsername not found. {3 - counter} attempt(s) left.\n\033[0m")
        counter += 1
        if counter == 4:
            print("\033[31mToo many failed attempts. Access denied.\n\033[0m")

# Main function that drives the CLI menu
def main():
    display_message("Welcome to PyAuth System")
    while True:
        print("--- Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        try:
            main_menu = int(input("Enter 1/2/3: "))
        except ValueError:
            print("\033[31mInvalid Input. Please enter a valid input.\n\033[0m")
        else:
            match main_menu:
                case 1:
                    registration()
                case 2:
                    login()
                case 3:
                    print("\033[32mExit successful\033[0m")
                    return

main()          
                  
