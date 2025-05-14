def display_message(user_text):
    box_width = 36
    text = user_text
    padding = (box_width - len(text) - 2) // 2
    print("=" * box_width)
    print("|" + " " * padding + text + " " * (box_width - len(text) - padding - 2) + "|")
    print("=" * box_width)

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
                    print("Registration function comig soon")
                case 2:
                    print("Login function coming soon")
                case 3:
                    print("Exit successful")
                    return

main()          
                  
