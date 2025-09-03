# 📚 Library Management System

A **Django-based Library Management System** designed for managing books, students, and admins.  

---

## 🚀 Features

### 👨‍💻 Admin Features
- Admin login with hardcoded credentials:  
  **Email:** `admin@gmail.com`  
  **Password:** `admin123`
- Admin Dashboard with full control.
- Add, update, and delete books.
- View all registered students.
- Manage issued books (track issued & returned).
- Post notices for students.

---

### 🎓 Student Features
- Student signup & login (session-based authentication).
- Browse and view available books.
- Request and issue a book.
- View issued books & pending returns.
- View notices posted by admin.
- Update personal profile (email, phone, password).

---

### 📦 Common Features
- Clean and responsive UI with **Bootstrap + custom CSS**.
- Session-based login system (**no Django default auth**).
- Error handling for invalid login/signup.
- Database: **SQLite3** (default, no setup required).
- Modular project structure (separate apps, templates, static files).


