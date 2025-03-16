from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models import Base, Student
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

@app.get("/students/by_faculty/{faculty}")
async def get_students_by_faculty(faculty: str, db:SessionLocal = Depends(get_db)):
    """
    Получить список студентов по названию факультета.
    """
    students = db.query(Student).filter(Student.faculty == faculty).all()
    if not students:
        raise HTTPException(status_code=404, detail=f"No students found for faculty {faculty}")
    return [{"id": s.id, "last_name": s.last_name, "first_name": s.first_name, "course": s.course, "grade": s.grade} for s in students]

@app.get("/courses/unique")
async def get_unique_courses(db:SessionLocal = Depends(get_db)):
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
