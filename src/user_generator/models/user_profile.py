# src/user-generator/models/user_profile.py
class UserProfile:
    def __init__(self, profile_type, poi_preferences, max_distance, transport_mean):
        self.profile_type = profile_type
        self.poi_preferences = poi_preferences
        self.max_distance = max_distance
        self.transport_mean = transport_mean

    def __repr__(self):
        return f"UserProfile({self.profile_type}, transport={self.transport_mean})"