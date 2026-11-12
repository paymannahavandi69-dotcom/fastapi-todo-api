from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import shutil
import os

app = FastAPI()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

engine = create_engine("sqlite:///todo.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String, default="")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    done = Column(Boolean, default=False)
    owner = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def register(user: UserCreate):
    session = Session()
    existing = session.query(User).filter(User.username == user.username).first()
    if existing:
        session.close()
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": "User registered"}

@app.post("/login")
def login(user: UserCreate):
    session = Session()
    db_user = session.query(User).filter(User.username == user.username).first()
    session.close()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks")
def get_tasks(username: str = Depends(get_current_user)):
    session = Session()
    tasks = session.query(Task).filter(Task.owner == username).all()
    result = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    session.close()
    return result

@app.post("/tasks")
def create_task(task: TaskCreate, username: str = Depends(get_current_user)):
    session = Session()
    new_task = Task(title=task.title, owner=username)
    session.add(new_task)
    session.commit()
    session.close()
    return {"message": "Task created", "title": task.title}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, username: str = Depends(get_current_user)):
    session = Session()
    task = session.query(Task).filter(Task.id == task_id, Task.owner == username).first()
    if not task:
        session.close()
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    session.close()
    return {"message": f"Task {task_id} deleted"}

@app.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    username: str = Depends(get_current_user)
):
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    
    file_path = f"uploads/{username}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    user.avatar = file_path
    session.commit()
    session.close()
    
    return {"message": f"Avatar uploaded for {username}"}
