import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_generator import RandomUserGenerator

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

names_path = os.path.join(BASE, "data", "names.json")
categories_path = os.path.join(BASE, "data", "category_poi.json")

gen = RandomUserGenerator(names_path, categories_path)
user = gen.generate_user()

print(user.to_dict())