from datetime import datetime
from uuid import uuid4

class User:
    def __init__(self, first_name, last_name, sex, username, profile_id, date_creation, Longitude, Latitude):
        self.user_id = str(uuid4())
        self.profile_id = profile_id
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.username = username
        self.date_creation = date_creation
        self.Longitude = Longitude
        self.Latitude = Latitude

    def to_dict(self):
        return {
            "User_id": self.user_id,
            "Profile_id": self.profile_id,
            "User_name": f"{self.first_name} {self.last_name}",
            "Username": self.username,
            "Sex": self.sex,
            "Date_creation": self.date_creation,
            "Longitude": self.Longitude,
            "Latitude": self.Latitude
        }