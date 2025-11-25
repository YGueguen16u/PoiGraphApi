# src/user-generator/src/user_generator.py

import random
import unicodedata

from models.user_profile import UserProfile
from models.user import User
from utils.file_loader import load_json
from utils.name_generator import generate_username


class RandomUserGenerator:
    def __init__(self, names_path: str, categories_path: str):
        """
        Initialise le générateur avec :
        - names.json (prénoms/nom)
        - category_poi.json (catégories POI par thème)
        """
        self.names = load_json(names_path)
        self.poi_categories = load_json(categories_path)
        self.existing_usernames = set()

        # Profils possibles (exemples)
        self.profile_types = [
            "food_lover",
            "sport_addict",
            "culture_seeker",
            "nightlife",
            "shopping",
            "balanced"
        ]

        # Moyens de transport
        self.transport_means = ["walk", "bike", "car", "public_transport"]

    # Utility: normalize text (remove accents, spaces, lowercase)
    def normalize_city(self, name):
        name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
        return "".join(c for c in name if c.isalnum()).lower()

    # Generate random profile
    def _generate_profile(self):
        profile_type = random.choice(self.profile_types)

        # Sélection de préférences POI selon le profil
        poi_preferences = self._select_poi_preferences(profile_type)

        max_distance = random.choice([500, 1000, 2000, 5000])  # mètres
        transport_mean = random.choice(self.transport_means)

        return UserProfile(
            profile_type=profile_type,
            poi_preferences=poi_preferences,
            max_distance=max_distance,
            transport_mean=transport_mean
        )

    # POI preferences based on profile type
    def _select_poi_preferences(self, profile_type):
        """
        Sélection fortement orientée tourisme et culture.
        """
        preferences = []

        for main_cat, groups in self.poi_categories.items():
            for thematic_group, subcats in groups.items():

                thematic_group_lower = thematic_group.lower()

                if "tourism" in thematic_group_lower or \
                "culture" in thematic_group_lower or \
                "art" in thematic_group_lower or \
                "museum" in thematic_group_lower or \
                "viewpoint" in thematic_group_lower:
                    preferences.extend(subcats)


                # food + tourism
                if profile_type == "food_lover":
                    if "food" in thematic_group_lower or "restaurant" in thematic_group_lower:
                        preferences.extend(subcats)

                # sport_addict
                elif profile_type == "sport_addict":
                    if "fitness" in thematic_group_lower or "sports" in thematic_group_lower:
                        preferences.extend(subcats)

                # culture + arts + tourism
                elif profile_type == "culture_seeker":
                    if "culture" in thematic_group_lower or "tourism" in thematic_group_lower \
                    or "art" in thematic_group_lower or "museum" in thematic_group_lower:
                        preferences.extend(subcats)

                # late-attraction + tourism
                elif profile_type == "nightlife":
                    if "bar" in thematic_group_lower or "nightclub" in thematic_group_lower:
                        preferences.extend(subcats)

                # shops + commercial tourism
                elif profile_type == "shopping":
                    if "clothing" in thematic_group_lower or "mall" in thematic_group_lower:
                        preferences.extend(subcats)

                elif profile_type == "balanced":
                    # 50% de chance d’ajouter tous les sous-groupes tourisme/culture
                    if "tourism" in thematic_group_lower or "culture" in thematic_group_lower:
                        preferences.extend(subcats)
                    else:
                        # 10% pour les autres POI
                        if random.random() < 0.1:
                            preferences.extend(subcats)

        # Nettoyage doublons
        preferences = list(set(preferences))

        # fallback minimal
        if not preferences:
            preferences = ["museum", "park", "viewpoint"]

        return preferences

    # Main method: generate a user
    def generate_user(self):
        # Sex
        sex = random.choice(["male", "female"])

        if sex == "male":
            first_name = random.choice(self.names["male_first_names"])
        else:
            first_name = random.choice(self.names["female_first_names"])

        last_name = random.choice(self.names["last_names"])

        # Username
        username = generate_username(first_name, last_name, self.existing_usernames)

        # Profile
        profile = self._generate_profile()

        # Position géographique (temporaire : random sur Montpellier)
        Longitude = 3.8767 + random.uniform(-0.02, 0.02)
        Latitude = 43.6108 + random.uniform(-0.02, 0.02)

        # User object
        return User(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            username=username,
            profile=profile,
            Longitude=Longitude,
            Latitude=Latitude
        )