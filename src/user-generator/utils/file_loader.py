# src/user-generator/utils/file_loader.py

import json
from pathlib import Path

def load_json(file_path: str):
    """
    Charge un fichier JSON depuis le chemin donné.
    Renvoie un dictionnaire Python.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erreur de lecture JSON dans {file_path}: {e}")