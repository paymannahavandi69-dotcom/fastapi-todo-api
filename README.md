# FastAPI To-Do API
A comprehensive API built with FastAPI and Python.

## Features
- **CRUD Operations**: Create, Read, and Delete tasks.
- **Database**: SQLAlchemy with SQLite for persistent storage.
- **Authentication**: User registration and login with hashed passwords (Bcrypt).
- **Security**: JWT (JSON Web Tokens) for secure route protection.
- **Error Handling**: Custom HTTP exceptions (404, 401, 400).

## Technologies Used
- Python
- FastAPI
- Pydantic (Data Validation)
- SQLAlchemy (Database ORM)
- SQLite (Persistent Database)
- Passlib & Bcrypt (Password Hashing)
- Python-Jose (JWT)

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn server:app --reload`
3. Open docs: `http://127.0.0.1:8000/docs`
