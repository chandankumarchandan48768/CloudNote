# 🗂️ CloudNote – Online Notes Storage System

CloudNote is a Django-based web app that helps students upload, organize, and retrieve academic notes. It integrates with Google Drive for cloud-based secure storage.

---

## 🚀 Features

- 📁 Upload and store notes online
- 🔒 Google Drive-based secure storage
- 👨‍🎓 Student & admin views
- 📑 Categorize by subject, branch, semester
- 🔐 User authentication

---

## 🖼️ Screenshots

### 📌 Home Page
![Home Page](screenshots/homepage.png)

### 📤 Upload Page
![Upload Page](screenshots/upload.png)

### 📁 Notes Listing
![Notes List](screenshots/notes-list.png)

---

## ⚙️ Tech Stack

- **Frontend**: HTML5, CSS, Bootstrap
- **Backend**: Django (Python)
- **Database**: SQLite
- **Cloud Storage**: Google Drive API

---

## 🛠️ Setup Instructions

```bash
git clone git@github.com:chandankumarchandan48768/CloudNote.git
cd CloudNote
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
