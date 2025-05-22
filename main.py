# Function to display a styled message box
def display_message(user_text):
    box_width = 36
    text = user_text
    padding = (box_width - len(text) - 2) // 2
    print("=" * box_width)
    print("|" + " " * padding + text + " " * (box_width - len(text) - padding - 2) + "|")
    print("=" * box_width)

# Stores existing users and their passwords (in-memory storage for now)
user_details = {
    "demo_user": "demo123"
}

# Registration function
def registration():
    print("\n")
    display_message("Register Here!")
    while True:
        username = input("Username: ")
        if username in user_details:
            print("User already exists. Please enter another username.\n")
        else:
            password = input("Password: ")
            user_details[username] = password
            print("Registration Successful!\n")
            break

# Password change function
def change_password(username):
    print("\n")
    display_message("Change Password")
    old_password = input("Old Password: ")
    if user_details[username] == old_password:
        new_password = input("New Password: ")
        user_details[username] = new_password
        print("Password changed Successfully.")
    else:
        print("Incorrect Password. Please try again.\n")

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
                        print("Invalid input.\n")
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
                            print("You have been logged out successfully.\n")
                            break
                        case _:
                            print("Invalid option.\n")
                break
            else:
                print(f"Incorrect password. {3 - counter} attempt(s) left.\n")
        else:
            if counter < 3:
                print(f"Username not found. {3 - counter} attempt(s) left.\n")

        counter += 1
        if counter == 4:
            print("Too many failed attempts. Access denied.\n")

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
            print("Invalid Input. Please enter a valid input.\n")
        else:
            match main_menu:
                case 1:
                    registration()
                case 2:
                    login()
                case 3:
                    print("Exit successful")
                    return

main()          
                  
