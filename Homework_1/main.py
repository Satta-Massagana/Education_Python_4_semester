import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    """Hello world!"""
    return {"Hello world!"}

@app.get("/add")
async def add(num1: float, num2: float):
    """Сложение двух чисел"""
    return {"result": num1 + num2}

@app.get("/subtract")
async def subtract(num1: float, num2: float):
    """Вычитание двух чисел"""
    return {"result": num1 - num2}

@app.get("/multiply")
async def multiply(num1: float, num2: float):
    """Умножение двух чисел"""
    return {"result": num1 * num2}

@app.get("/divide")
async def divide(num1: float, num2: float):
    """Деление двух чисел"""
    if num2 == 0:
        return {"error": "Cannot divide by zero"}
    return {"result": num1 / num2}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=444,
        reload=True
    )