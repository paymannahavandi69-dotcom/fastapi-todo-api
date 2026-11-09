from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

engine = create_engine("sqlite:///school.db")
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str

@app.post("/students")
def create_student(student: StudentCreate):
    session = Session()
    new_student = Student(name=student.name, age=student.age, grade=student.grade)
    session.add(new_student)
    session.commit()
    session.close()
    return {"message": "Student created"}

@app.get("/students")
def get_students():
    session = Session()
    students = session.query(Student).all()
    result = []
    for s in students:
        result.append({"id": s.id, "name": s.name, "age": s.age, "grade": s.grade})
    session.close()
    return result
