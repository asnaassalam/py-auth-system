import customtkinter
import subprocess
import sys
import re
import tkinter.messagebox as mbox
import json
import hashlib
import os



def show_welcome(username):
    welcome = customtkinter.CTk()
    welcome.title("PY-AUTH-SYSTEM")
    welcome.geometry("1200x650")
    welcome.configure(bg="#e6f0fa")

    # Welcome label
    label = customtkinter.CTkLabel(
        master=welcome,
        text=f"Welcome, {username}!",
        font=("Arial", 32, "bold"),
        text_color="#1976d2"
    )
    label.place(relx=0.5, rely=0.3, anchor="center")

    # Frame to hold buttons and form
    action_frame = customtkinter.CTkFrame(master=welcome, fg_color="transparent")
    action_frame.place(relx=0.5, rely=0.45, anchor="center")

    # Function to logout
    def logout():
        welcome.destroy()
        subprocess.Popen([sys.executable, "gui-version/login.py"])

    # Function to show reset password form
    def show_reset_form():
        form_frame.place(relx=0.5, rely=0.7, anchor="center")

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def reset_password():
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        # Load users.json at the start
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                user_details = json.load(f)
        else:
            user_details = {}

        # Check if username exists
        if username not in user_details:
            mbox.showerror("Error", "User does not exist.")
            return

        # Check if both fields are filled
        if not password or not confirm_password:
            mbox.showerror("Error", "Please fill in both fields")
            return

        # Validation logic for password strength
        if len(password) < 8 or \
        not re.search(r'[A-Z]', password) or \
        not re.search(r'[a-z]', password) or \
        not re.search(r'\d', password) or \
        not re.search(r'[^\w\s]', password):
            mbox.showerror(
                "Error",
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character"
            )
            return

        # Check if new password is same as old password
        old_password_hash = user_details[username]
        if hash_password(password) == old_password_hash:
            mbox.showerror("Error", "New password cannot be the same as the old password")
            return
        
        # Check if passwords match 
        if password != confirm_password:
            mbox.showerror("Error", "Passwords do not match")
            return
            
        # Update password
        user_details[username] = hash_password(password)

        # Save back to users.json
        with open("users.json", "w") as f:
            json.dump(user_details, f, indent=4)

        mbox.showinfo("Success", "Password reset successfully")
        form_frame.place_forget()


    # Buttons
    reset_btn = customtkinter.CTkButton(
        master=action_frame,
        text="Reset Password",
        width=180,
        height=50,
        font=("Arial", 19, "bold"),
        fg_color="#ff9800",  
        hover_color="#fb8c00",
        text_color="white",
        command=show_reset_form
    )
    reset_btn.grid(row=0, column=0, padx=10, pady=10)

    logout_btn = customtkinter.CTkButton(
        master=action_frame,
        text="Logout",
        width=180,
        height=50,
        font=("Arial", 19, "bold"),
        fg_color="#1976d2",  
        hover_color="#1565c0",
        text_color="white",
        command=logout
    )
    logout_btn.grid(row=0, column=1, padx=10, pady=10)

    form_frame = customtkinter.CTkFrame(
        master=welcome,
        fg_color="#d6e7f4",
        corner_radius=20,
        width=520,
        height=180
    )

    password_label = customtkinter.CTkLabel(
        form_frame,
        text="New Password:",
        font=("Arial", 18, "bold"),
        text_color="#1976d2",
        fg_color="#d6e7f4"
    )
    password_label.grid(row=0, column=0, padx=20, pady=15, sticky="e")

    password_entry = customtkinter.CTkEntry(
        form_frame,
        show="*",
        width=350,
        height=45,
        fg_color="#d6e7f4",
        border_color="#6fbcf3",
        border_width=2,
        text_color="#0d47a1",
        font=("Arial", 16),
        placeholder_text="Enter new password",
        placeholder_text_color="#90caf9"
    )
    password_entry.grid(row=0, column=1, padx=20, pady=15)

    confirm_label = customtkinter.CTkLabel(
        form_frame,
        text="Confirm Password:",
        font=("Arial", 18, "bold"),
        text_color="#1976d2",
        fg_color="#d6e7f4"
    )
    confirm_label.grid(row=1, column=0, padx=20, pady=15, sticky="e")

    confirm_entry = customtkinter.CTkEntry(
        form_frame,
        show="*",
        width=350,
        height=45,
        fg_color="#d6e7f4",
        border_color="#6fbcf3",
        border_width=2,
        text_color="#0d47a1",
        font=("Arial", 16),
        placeholder_text="Confirm new password",
        placeholder_text_color="#90caf9"
    )
    confirm_entry.grid(row=1, column=1, padx=20, pady=15)

    submit_btn = customtkinter.CTkButton(
        form_frame,
        text="Submit",
        width=360,
        height=50,
        fg_color="#1976d2",  
        hover_color="#1565c0",
        font=("Arial", 18, "bold"),
        command=reset_password
    )
    submit_btn.grid(row=2, column=0, columnspan=2, pady=(10, 20))

    form_frame.place_forget()  


    welcome.mainloop()


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "User"
    show_welcome(username)

