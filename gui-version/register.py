import customtkinter
import json
import hashlib
import tkinter.messagebox as mbox
import subprocess
import sys
import re

# Load user details from JSON 
try:
    with open("users.json", "r") as file1:
        user_details = json.load(file1)
except FileNotFoundError:
    user_details = {}

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate username
def validateUsername(username, user_details=user_details):
    if not username:
        return "Username is required."
    elif username in user_details:
        return "User already exists. Please enter another username."     
    elif len(username) < 8:
        return "Username must be at least 8 characters."
    elif " " in username:
        return "Username cannot contain spaces."
    elif not re.match(r'^[a-z0-9_]+$', username):
        return "Username can only contain lowercase letters, numbers, and underscores."
    return None  

# Function to validate password
def validatePassword(password):
    if not password:
        return "Password is required."  
    elif len(password) < 6:
        return "Password must be at least 6 characters long."
    elif not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    elif not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    elif not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."
    elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return "Password must contain at least one special character."
    return None          

# Set appearance mode and color theme
customtkinter.set_appearance_mode("#e9f1fa")
customtkinter.set_default_color_theme("blue")

# Create the main window
register = customtkinter.CTk()
register.title("PY-AUTH-SYSTEM")
register.geometry("1200x650")
register.configure(bg="#e6f0fa")

# Create input frame for registration
input_frame = customtkinter.CTkFrame(
    master=register,
    width=500,
    height=500,
    corner_radius=20,
    fg_color="#d6e7f4",
    border_color="#6fbcf3",
    border_width=3
)
input_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title for registration form
title_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Register Now",
    font=("Arial", 35, "bold"),
    text_color="#113051",
    justify="center"
)
title_label.place(relx=0.5, rely=0.13, anchor="center")

# Subtitle for registration form
subtitle_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Create your account to get started!",
    font=("Arial", 21),
    text_color="#1565c0",
    justify="center"
)
subtitle_label.place(relx=0.5, rely=0.2, anchor="center")

# Create labels and entries for username
username_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Username:",
    font=("Arial", 18, "bold"),
    text_color="#1976d2",
    fg_color="#d6e7f4"
)
username_label.place(relx=0.19, rely=0.31, anchor="center")

username_entry = customtkinter.CTkEntry(
    master=input_frame,
    width=400,
    height=45,
    placeholder_text="Enter your username",
    fg_color="#d6e7f4",
    border_color="#6fbcf3",
    border_width=2,
    text_color="#0d47a1",
    font=("Arial", 16),
    placeholder_text_color="#90caf9"
)
username_entry.place(relx=0.5, rely=0.38, anchor="center")

# Create labels and entries for password
password_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Password:",
    font=("Arial", 18, "bold"),
    text_color="#1976d2",
    fg_color="#d6e7f4"
)
password_label.place(relx=0.19, rely=0.48, anchor="center")

password_entry = customtkinter.CTkEntry(
    master=input_frame,
    width=400,
    height=45,
    placeholder_text="Enter your password",
    show="*",
    fg_color="#d6e7f4",
    border_color="#6fbcf3",
    border_width=2,
    text_color="#0d47a1",
    font=("Arial", 16),
    placeholder_text_color="#90caf9"
)
password_entry.place(relx=0.5, rely=0.55, anchor="center")

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        eye_button.configure(text="🙈")  
    else:
        password_entry.configure(show="*")
        eye_button.configure(text="🙉")  

eye_button = customtkinter.CTkButton(
    master=input_frame,
    text="🙉",  
    width=0,
    height=0,
    font=("Arial", 25),
    fg_color="#d6e7f4",
    text_color="#1976d2",
    hover_color="#1565c0",
    cursor="hand2",
    command=toggle_password
)
eye_button.place(relx=0.85, rely=0.545, anchor="center")

# Register button
register_button = customtkinter.CTkButton(
    master=input_frame,
    text="Sign Up",
    width=370,
    height=50,
    font=("Arial", 22, "bold"),
    fg_color="#1976d2",
    hover_color="#1565c0",
    text_color="white",
    cursor="hand2"
)
register_button.place(relx=0.5, rely=0.69, anchor="center")

# Link to login page
def open_login():
    register.destroy() 
    subprocess.Popen([sys.executable, "gui-version/login.py"])

# Link label for login
login_link_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Already have an account? Login",
    font=("Arial", 16, "italic"),
    text_color="#1976d2",
    cursor="hand2"
)
login_link_label.place(relx=0.5, rely=0.79, anchor="center")
login_link_label.bind("<Button-1>", lambda e: open_login())

# Handle registration function
def handle_register():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    username_error = validateUsername(username)
    if username_error:
        mbox.showerror("Registration Error", username_error)
        return
    password_error = validatePassword(password)
    if password_error:
        mbox.showerror("Registration Error", password_error)
        return
    user_details[username] = hash_password(password)
    with open("users.json", "w") as file2:
        json.dump(user_details, file2, indent=4)
    mbox.showinfo("Success", "Registration Successful!")
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")
    open_login()  

register_button.configure(command=handle_register)    
register.mainloop()