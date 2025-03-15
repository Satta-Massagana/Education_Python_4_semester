from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, field_validator
from datetime import datetime
import uvicorn
import json
import re

app = FastAPI()

# Модель для валидации данных
class Abonent(BaseModel):
    surname: str
    name: str
    birth_date: str
    phone_number: str
    email: str

    @field_validator('surname', 'name')
    def check_name(cls, v):
        if not re.match(r'^[А-Я][а-я]*$', v):
            raise ValueError('Фамилия/Имя должны начинаться с заглавной буквы и содержать только кирилицу')
        return v

    @field_validator('birth_date')
    def check_birth_date(cls, v):
        try:
            datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Дата рождения должна быть в формате DD-MM-YYYY')
        return v

    @field_validator('phone_number')
    def check_phone_number(cls, v):
        if not re.match(r'^\+7\d{10}$', v):
            raise ValueError('Номер телефона должен начинаться с +7 и содержать 10 цифр')
        return v

    @field_validator('email')
    def check_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
            raise ValueError('Некорректный формат электронной почты')
        return v

# Эндпойнт для сбора обращений
@app.post("/abonent/")
async def create_abonent(abonent: Abonent):
    try:
        # Сохраняем данные в JSON-файл
        with open('.\\Homework_2\\abonents.json', 'a', encoding='utf-8') as f:
            json.dump(abonent.model_dump(), f, ensure_ascii=False)
            f.write('\n')
        return {"message": "Обращение успешно сохранено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=444,
        reload=True
    )