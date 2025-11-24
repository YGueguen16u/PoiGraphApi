# src/user-generator/utils/name_generator.py
import random
import string

def generate_username(first_name: str, last_name: str, existing_usernames: set) -> str:
    base_username = (first_name[0] + last_name).lower().replace(" ", "")
    username = base_username

    while username in existing_usernames:
        suffix = ''.join(random.choices(string.digits, k=2))
        username = f"{base_username}{suffix}"

    existing_usernames.add(username)
    return username
    
