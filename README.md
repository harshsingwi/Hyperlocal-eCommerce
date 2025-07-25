# 🛒 MahendraStores

MahendraStores is a Django-based e-commerce web application designed to manage online product listings, user authentication, and orders efficiently.

---

## 📌 Features

- User registration and authentication (Login/Logout)
- Product catalog with images and details
- Cart and order management
- Admin panel for product and user management
- SQLite database for development

---

## 🏗️ Tech Stack

- **Backend**: Python, Django
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap
- **Version Control**: Git

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ecomproject
```

### 2. Create a virtual environment and activate it

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

*(If `requirements.txt` is not available, manually install Django:)*

```bash
pip install django
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🧑‍💻 Admin Access

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Then go to `http://127.0.0.1:8000/admin` and log in with the superuser credentials.

---

## 📁 Project Structure

```
ecomproject/
│
├── manage.py
├── db.sqlite3
├── app/                  # Your main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
└── .git/                 # Git version control
```

---

## 📦 Deployment

You can deploy this project on platforms like:

- [Render](https://render.com/)
- [Heroku](https://www.heroku.com/)
- [PythonAnywhere](https://www.pythonanywhere.com/)

---

## 📜 License

This project is licensed under the MIT License - feel free to use and modify it.

---

## 🙌 Acknowledgements

Special thanks to the Django community and Bootstrap for their awesome tools.
