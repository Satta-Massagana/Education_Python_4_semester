from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models import Base, Student
from pydantic import BaseModel
import uvicorn
import csv

app = FastAPI()

# Подключение к PostgreSQL
DATABASE_URL = "postgresql://admin1:ASqw12@localhost:5433/admin1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц при запуске приложения
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_data_from_csv():
    session = SessionLocal()
    
    # Проверка наличия данных в базе данных
    if session.query(Student).first() is None:
        with open('./Homework_3/students.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = Student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=float(row['Оценка'])
                )
                session.add(student)
        session.commit()
    session.close()

@app.on_event("startup")
async def startup_event():
    load_data_from_csv()

# Pydantic-модель для создания нового студента
class StudentCreate(BaseModel):
    last_name: str
    first_name: str
    faculty: str
    course: str
    grade: float

# Pydantic-модель для обновления существующего студента
class StudentUpdate(BaseModel):
    last_name: str | None
    first_name: str | None
    faculty: str | None
    course: str | None
    grade: float | None

# CRUD операции

@app.post("/students/")
async def create_student(student: StudentCreate, db: SessionLocal = Depends(get_db)):
    """
    Создать новую запись о студенте.
    """
    new_student = Student(
        last_name=student.last_name,
        first_name=student.first_name,
        faculty=student.faculty,
        course=student.course,
        grade=student.grade
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"id": new_student.id, "last_name": new_student.last_name, "first_name": new_student.first_name, "course": new_student.course, "grade": new_student.grade}

@app.get("/students/{student_id}")
async def read_student(student_id: int, db: SessionLocal = Depends(get_db)):
    """
    Получить информацию о студенте по ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return {"id": student.id, "last_name": student.last_name, "first_name": student.first_name, "course": student.course, "grade": student.grade}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate, db: SessionLocal = Depends(get_db)):
    """
    Обновить информацию о студенте.
    """
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    
    existing_student.last_name = student.last_name or existing_student.last_name
    existing_student.first_name = student.first_name or existing_student.first_name
    existing_student.faculty = student.faculty or existing_student.faculty
    existing_student.course = student.course or existing_student.course
    existing_student.grade = student.grade or existing_student.grade
    
    db.commit()
    db.refresh(existing_student)
    return {"id": existing_student.id, "last_name": existing_student.last_name, "first_name": existing_student.first_name, "course": existing_student.course, "grade": existing_student.grade}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: SessionLocal = Depends(get_db)):
    """
    Удалить запись о студенте по ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    db.delete(student)
    db.commit()
    return {"message": f"Student with ID {student_id} has been deleted"}

@app.get("/students/by_faculty/{faculty}")
async def get_students_by_faculty(faculty: str, db: SessionLocal = Depends(get_db)):
    """
    Получить список студентов по названию факультета.
    """
    students = db.query(Student).filter(Student.faculty == faculty).all()
    if not students:
        raise HTTPException(status_code=404, detail=f"No students found for faculty {faculty}")
    return [{"id": s.id, "last_name": s.last_name, "first_name": s.first_name, "course": s.course, "grade": s.grade} for s in students]

@app.get("/courses/unique")
async def get_unique_courses(db: SessionLocal = Depends(get_db)):
    """
    Получить список уникальных курсов.
    """
    courses = db.query(Student.course).distinct().all()
    return {"unique_courses": [course[0] for course in courses]}

@app.get("/faculty/average_grade/{faculty}")
async def get_average_grade_by_faculty(faculty: str, db: SessionLocal = Depends(get_db)):
    """
    Получить средний балл по факультету.
    """
    avg_grade = db.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()
    if avg_grade is None:
        raise HTTPException(status_code=404, detail=f"No grades found for faculty {faculty}")
    return {"faculty": faculty, "average_grade": round(avg_grade, 2)}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=444
    )
