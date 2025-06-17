# Import json module
import json
# Import hashlib module for password hashing using SHA-256
import hashlib

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

# Loads existing users from users.json file
with open("users.json", "r") as file1:
    user_details = json.load(file1)

# Registration function
def registration():
    print("\n")
    display_message("Register Here!")
    while True:
        username = input("Username: ").strip()
        if not username:
            print("\033[31mUsername can not be empty.\033[0m")
            continue
        if username in user_details:
            print("\033[31mUser already exists. Please enter another username.\n\033[0m")
        while True:
            password = input("Password: ").strip()
            if not password:
                print("\033[31mPassword can not be empty.\033[0m")
                continue
            else:
                user_details[username] = password
                with open("users.json", "w") as file2:
                    json.dump(user_details, file2, indent=4)
                    print("\033[32mRegistration Successful!\n\033[0m")
                return

# Password change function
def change_password(username):
    print("\n")
    display_message("Change Password")
    old_password = input("Old Password: ")
    if user_details[username] == old_password:
        new_password = input("New Password: ")
        user_details[username] = new_password
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
            if user_details[username] == password:
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
                  
