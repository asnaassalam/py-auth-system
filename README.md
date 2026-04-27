# 🔐 Py Auth System

A step-by-step evolving project that begins as a simple CLI-based login/register app and gradually transforms into a fully secure, cloud-hosted authentication system with REST API and JWT.

> 🌿 Each phase lives in its own branch. `main` always reflects the latest complete version.

---

## 🌿 Branch Structure

| Branch | Description | Status |
|---|---|---|
| `v1-functional` | Original functional version (CLI + GUI) | ✅ Complete |
| `feature/oop` | OOP refactor with clean class structure | ✅ Complete |
| `feature/jwt` | REST API with FastAPI and JWT auth | 🔜 Coming Soon |
| `feature/aws` | Cloud deployment on AWS | 🔜 Coming Soon |

---

## 🚀 Project Phases

### ✅ Phase 1 — Functional Version (`v1-functional`)
- [x] CLI register, login, profile, change password
- [x] JSON file storage
- [x] Password hashing with `hashlib`
- [x] Input validation
- [x] GUI with `customtkinter`

### 🔄 Phase 2 — OOP Refactor (`feature/oop`)
- [x] `User` class with properties and setters
- [x] `Validator` class for all validation rules
- [x] `FileStorage` class for JSON read/write
- [x] `AuthManager` class coordinating all logic
- [x] Rebuilt GUI with `tkinter`

### 🔜 Phase 3 — REST API + JWT (`feature/jwt`)
- [ ] FastAPI backend
- [ ] JWT authentication
- [ ] MySQL database with SQLAlchemy ORM
- [ ] Bcrypt password hashing
- [ ] Pydantic request validation
- [ ] CORS and environment variable configuration

### 🔜 Phase 4 — Cloud Deployment (`feature/aws`)
- [ ] Dockerized application
- [ ] AWS EC2 + RDS (MySQL) deployment
- [ ] SSL certificate via ACM
- [ ] GitHub Actions CI/CD pipeline

---

## 🛠️ Tech Stack

| Phase | Tools |
|---|---|
| Phase 1 | Python, `hashlib`, `json`, `customtkinter` |
| Phase 2 | Python OOP, `tkinter` |
| Phase 3 | FastAPI, JWT, MySQL, SQLAlchemy, Bcrypt, PyMySQL |
| Phase 4 | Docker, AWS EC2, AWS RDS, GitHub Actions |

---

## 📁 Folder Structure

```
py-auth-system/
├── oop_version/
│   ├── auth_gui.py        # tkinter GUI
│   ├── auth_manager.py    # Register and login logic
│   ├── file_storage.py    # JSON read/write
│   ├── user.py            # User class with properties and setters
│   └── validator.py       # All validation rules
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Setup & Installation

> **Prerequisites:** Python 3.x — tkinter is included with Python by default, no installation needed.

**1. Clone the repository**
```bash
git clone https://github.com/asnaassalam/py-auth-system.git
cd py-auth-system
```

---

## ▶️ How to Run

### Current Version (OOP — Phase 2)
```bash
cd oop_version
python auth_gui.py
```

### Original Version (Functional — Phase 1)
Switch to the `v1-functional` branch:
```bash
git checkout v1-functional
```
Then follow the instructions in that branch's README.

---

## ✅ Best Practices Followed
- Passwords are **hashed** before storing — never saved as plaintext
- **Input validation** enforced on both frontend and backend layers
- Clear **separation of concerns** — each class has one job
- Sensitive files like `users.json` are **excluded from version control**

---

## 📌 Notes
- `users.json` is excluded from the repo via `.gitignore` — it is generated locally on first run

---

## 🧠 Concepts Covered
- File Handling and JSON Persistence
- Password Hashing and Security
- Object Oriented Programming
- GUI Development with tkinter
- REST API Design (coming Phase 3)
- JWT Authentication (coming Phase 3)
- Cloud Deployment on AWS (coming Phase 4)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

## ✍️ Author
[Asna Assalam](https://github.com/asnaassalam)

> Built as part of my self-learning journey from beginner Python scripts to a full production-grade authentication system.
