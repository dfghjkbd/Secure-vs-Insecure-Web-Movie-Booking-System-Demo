# 🎬 Secure vs Insecure Web: Movie Booking System Demo

This Django-based project showcases how common web vulnerabilities such as **SQL Injection (SQLi)** and **Cross-Site Scripting (XSS)** can be exploited in insecure web applications. It also demonstrates how to properly secure these issues using Django's ORM and form validation.

---

## 🔍 Project Overview

The system allows users to register, log in, view movies, and book seats. It includes two versions:

- `/insecure/`: Implements vulnerable code to demonstrate exploitation.
- `/secure/`: Implements best practices to prevent security flaws.

---

## ❌ Insecure Version Highlights

- **SQL Injection** via login form using raw SQL queries.
- **Cross-Site Scripting (XSS)** vulnerability in user feedback rendering.
- No form validation or output sanitization.

## ✅ Secure Version Highlights

- Uses Django ORM for authentication (protects against SQLi).
- Escapes user input in templates to prevent XSS.
- Validates forms to avoid malicious input.
- Includes login protection for booking pages.

---

## 🎯 Purpose

This project is intended for educational use to:

- Demonstrate real-world attack vectors like SQL Injection and XSS.
- Compare insecure vs. secure implementation side by side.
- Help students and developers learn secure web development practices.

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML/CSS with Bootstrap
- **Security Concepts Covered:** SQL Injection, XSS

---






