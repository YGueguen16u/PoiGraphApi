# src/user-generator/app.py
from fastapi import FastAPI
from src.user_generator import RandomUserGenerator
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
names_path = os.path.join(BASE_DIR, "data", "names.json")
categories_path = os.path.join(BASE_DIR, "data", "category_poi.json")

generator = RandomUserGenerator(names_path, categories_path)

@app.get("/generate_user")
def generate_user():
    user = generator.generate_user()
    return user.to_dict()

 