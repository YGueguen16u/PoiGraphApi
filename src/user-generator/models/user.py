# src/user-generator/models/user.py

from uuid import uuid4

class User:
    def __init__(self, first_name, last_name, sex, username, profile, Longitude, Latitude):
        """
        Initialize a User object.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            sex (str): The sex of the user.
            username (str): The username of the user.
            profile (UserProfile): The profile of the user.
            Longitude (float): The longitude of the user.
            Latitude (float): The latitude of the user.
        """
        self.user_id = str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.username = username
        self.profile = profile
        self.Longitude = Longitude
        self.Latitude = Latitude

    def to_dict(self):
        return {
            "User_id": self.user_id,
            "User_name": f"{self.first_name} {self.last_name}",
            "Username": self.username,
            "Sex": self.sex,
            "Profile": self.profile.profile_type,
            "POI_preferences": self.profile.poi_preferences,
            "Longitude": self.Longitude,
            "Latitude": self.Latitude
        }