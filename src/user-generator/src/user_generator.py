# src/user-generator/src/user_generator.py

import random
import unicodedata
import csv

from models.user_profile import UserProfile
from models.user import User
from utils.file_loader import load_json
from utils.name_generator import generate_username


class RandomUserGenerator:
    def __init__(self, names_path: str, categories_path: str, poi_matrix_path: str):
        """
        Initialise le générateur avec :
        - names.json (prénoms/nom)
        - category_poi.json (catégories OSM — utile uniquement pour la liste des POI)
        - poi_profile_matrix.csv (matrice de probabilités profil → POI)
        """
        self.names = load_json(names_path)
        self.poi_categories = load_json(categories_path)
        self.existing_usernames = set()

        # Profils disponibles
        self.profile_types = [
            "food_lover",
            "sport_addict",
            "culture_seeker",
            "nightlife",
            "shopping",
            "balanced"
        ]

        # Transport
        self.transport_means = ["walk", "bike", "car", "public_transport"]

        # Chargement de la matrice des probabilités
        self.poi_prob_matrix = self._load_poi_matrix(poi_matrix_path)


    def _load_poi_matrix(self, matrix_path):
        matrix = {}

        with open(matrix_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)[1:]  # skip first column (profile name)

            for row in reader:
                profile = row[0].strip()
                probs = list(map(float, row[1:]))
                matrix[profile] = dict(zip(header, probs))

        return matrix


    def normalize_city(self, name):
        name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
        return "".join(c for c in name if c.isalnum()).lower()

    def _generate_profile(self):
        profile_type = random.choice(self.profile_types)
        poi_preferences = self._select_poi_preferences(profile_type)

        max_distance = random.choice([500, 1000, 2000, 5000])
        transport_mean = random.choice(self.transport_means)

        return UserProfile(
            profile_type=profile_type,
            poi_preferences=poi_preferences,
            max_distance=max_distance,
            transport_mean=transport_mean
        )


    def _select_poi_preferences(self, profile_type):
        prefs = []
        poi_probs = self.poi_prob_matrix[profile_type]

        for poi_name, prob in poi_probs.items():
            # tirage pondéré
            if random.random() < prob:
                prefs.append(poi_name)

        # Sécurité : éviter 0 POI
        if not prefs:
            # garder les POI avec proba forte
            prefs = [
                poi for poi, p in poi_probs.items()
                if p > 0.2
            ][:5]

        # unique
        return list(set(prefs))


    def generate_user(self):
        # Sexe
        sex = random.choice(["male", "female"])
        if sex == "male":
            first_name = random.choice(self.names["male_first_names"])
        else:
            first_name = random.choice(self.names["female_first_names"])

        last_name = random.choice(self.names["last_names"])

        # Username
        username = generate_username(first_name, last_name, self.existing_usernames)

        # Profil
        profile = self._generate_profile()

        # Localisation (temporaire : Montpellier)
        Longitude = 3.8767 + random.uniform(-0.02, 0.02)
        Latitude = 43.6108 + random.uniform(-0.02, 0.02)

        return User(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            username=username,
            profile=profile,
            Longitude=Longitude,
            Latitude=Latitude
        )