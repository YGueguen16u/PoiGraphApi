import sys, os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

sys.path.append(PROJECT_ROOT)

from user_generator import RandomUserGenerator

# chemins
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

names_path = os.path.join(DATA_DIR, "names.json")
categories_path = os.path.join(DATA_DIR, "category_poi.json")
poi_matrix_path = os.path.join(DATA_DIR, "poi_profile_matrix.csv")

# générateur
gen = RandomUserGenerator(
    names_path,
    categories_path,
    poi_matrix_path
)

# user
user = gen.generate_user()

print("User generated")
print(user.to_dict())