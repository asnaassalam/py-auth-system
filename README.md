# 🔐 Py Auth System

A step-by-step evolving project that begins as a simple CLI-based login/register app using Python dictionaries and gradually transforms into a secure, GUI-based user authentication system using file storage and password hashing.

## 🚀 Project Phases & Features

### ✅ Phase 1: CLI (In-Memory Dictionary)
- [x] Register new users
- [x] Login existing users
- [x] View user profile
- [x] Change/reset Password
- [x] Basic CLI interface

### ✅ Phase 2: File-Based Storage
- [x] Save user data in JSON file
- [x] Load data at startup
- [x] Prevent duplicate registrations

### ✅ Phase 3: Password Hashing
- [x] Secure password storage using `hashlib`
- [x] Password verification during login

### ✅ Phase 4: Input Validation
- [x] Validate username
- [x] Enforce password strength
- [x] Meaningful error messages

### ⏳ Phase 5: GUI with customtkinter
- [ ] Register/Login screens with modern UI  
- [ ] Message boxes for success/failure feedback  
- [ ] Password masking  
- [ ] Separate windows for Register, Login, and Welcome  
- [ ] Navigation between Register and Login screens  
- [ ] Change/reset password 
- [ ] Logout functionality

## 🛠️ Tech Stack
- Python 3.x  
- `hashlib` – for password hashing  
- `json` – for user data persistence  
- `customtkinter` – for modern and themed GUI components 

## 📁 Folder Structure
```
py-auth-system/
├── cli-version/              
│   └── main.py              # CLI-based logic
│
├── gui-version/
│   ├── register.py          # GUI Register window
│   ├── login.py             # GUI Login window
│   └── welcome.py           # Welcome window after login
│
├── users.json               # Shared user data file
└── README.md                # Project overview
```

## ▶️ How to Run

### 💻 CLI Version
1. Navigate to the `cli-version` folder:
   ```bash
   cd cli-version
   python main.py
   ```

---

### 🪟 GUI Version

> 🛑 Requires `customtkinter`. Install it first:

```bash
pip install customtkinter
```

2. Navigate to the `gui-version` folder:
   ```bash
   cd gui-version
   python register.py
   ```

> 🔄 You can navigate between **Register** and **Login** windows via links.  
> ✅ On successful login, a **Welcome** window will appear with a **Reset Password** and **Logout** button.

## ✅ Best Practices Followed

- Passwords are **hashed** before storing  
- Plaintext passwords are **never** saved  
- Includes **input validation** and **error handling**  
- Clear separation between **CLI** and **GUI** components  
- GUI code uses **modular window design**

## 📌 Notes

- The `users.json` file stores hashed passwords only. No plaintext passwords are stored.
- For demo/testing, use this default test account:
  - **Username**: `demo_user`
  - **Password**: `Demo@123`


## 🧠 Concepts Covered
- File Handling
- Password Hashing & Security
- JSON-based Data Persistence
- GUI Development with customtkinter
- Modular Python Code

## ✍️ Author
[Asna Assalam](https://github.com/asnaassalam)