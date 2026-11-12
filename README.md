# FastAPI To-Do API
A comprehensive RESTful API built with FastAPI and Python.

## Features
- **User Authentication**: Register and Login with JWT (JSON Web Tokens).
- **Security**: Passwords are hashed using Bcrypt.
- **Database**: SQLAlchemy with SQLite for persistent storage.
- **CRUD Operations**: Create, Read, and Delete tasks.
- **User Isolation**: Users can only see and delete their own tasks.
- **File Upload**: Users can upload avatars with size and type validation.
- **Error Handling**: Custom HTTP exceptions.

## Technologies Used
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Passlib & Bcrypt
- Python-Jose (JWT)
- Python-Multipart (File Uploads)

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn server:app --reload`
3. Open docs: `http://127.0.0.1:8000/docs`
