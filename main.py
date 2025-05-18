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
                    print("Login function coming soon")
                case 3:
                    print("Exit successful")
                    return

main()          
                  
