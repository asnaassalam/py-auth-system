import customtkinter
import json
import hashlib
import tkinter.messagebox as mbox
import subprocess
import sys

# Load user details from JSON
try:
    with open("users.json", "r") as file1:
        user_details = json.load(file1)
except FileNotFoundError:
    user_details = {}

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Set appearance mode and color theme
customtkinter.set_appearance_mode("#e9f1fa")
customtkinter.set_default_color_theme("blue")

# Create the main window
login = customtkinter.CTk()
login.title("PY-AUTH-SYSTEM")
login.geometry("1200x650")
login.configure(bg="#e6f0fa")

# Create input frame for login
input_frame = customtkinter.CTkFrame(
    master=login,
    width=500,
    height=500,
    corner_radius=20,
    fg_color="#d6e7f4",
    border_color="#6fbcf3",
    border_width=3
)
input_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title for login form 
title_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Login",
    font=("Arial", 35, "bold"),
    text_color="#113051",
    justify="center"
)
title_label.place(relx=0.5, rely=0.13, anchor="center")

# Subtitle for login form
subtitle_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Enter your credentials to login!",
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
        eye_button.configure(text="🙈")  # Hide password
    else:
        password_entry.configure(show="*")
        eye_button.configure(text="🙉")  # Show password

eye_button = customtkinter.CTkButton(
    master=input_frame,
    text="🙉",  # Start with show password icon
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

# Login button
login_button = customtkinter.CTkButton(
    master=input_frame,
    text="Sign In",
    width=370,
    height=50,
    font=("Arial", 22, "bold"),
    fg_color="#1976d2",
    hover_color="#1565c0",
    text_color="white",
    cursor="hand2"
)
login_button.place(relx=0.5, rely=0.69, anchor="center")

# Link to registration page
def open_register():
    login.destroy() 
    subprocess.Popen([sys.executable, "gui-version/register.py"])

# Link label for registration
register_link_label = customtkinter.CTkLabel(
    master=input_frame,
    text="Don't have an account? Register here",
    font=("Arial", 16, "italic"),
    text_color="#1976d2",
    cursor="hand2"
)
register_link_label.place(relx=0.5, rely=0.79, anchor="center")
register_link_label.bind("<Button-1>", lambda e: open_register())

# Handle login function
def handle_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        mbox.showerror("Error", "Username and password cannot be empty.")
        return
    if username in user_details:
        if user_details[username] == hash_password(password):
            login.destroy()
            subprocess.Popen([sys.executable, "gui-version/welcome.py", username])
        else:
            mbox.showerror("Error", "Incorrect password.")
    else:
        mbox.showerror("Error", "Username not found.")

login_button.configure(command=handle_login)        
login.mainloop()
