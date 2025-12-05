# src/osm/spark_osm/run_batch.py
import csv
import os
import unicodedata
from spark_osm.extractor import extract_city_poi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "annexe", "sub_categories.json")
output_dir = os.path.join(BASE_DIR, "output")
csv_path = os.path.join(BASE_DIR, "019HexaSmal.csv")

OCCITANIE_PREFIXES = (
    "09", "11", "12", "30", "31", "32", "34",
    "46", "48", "65", "66", "81", "82"
)

def normalize_city(name: str) -> str:
    name = name.strip()
    name = name.title()
    name = unicodedata.normalize("NFC", name)
    return name

communes = set()

with open(csv_path, newline='', encoding='latin-1') as f:
    reader = csv.reader(f, delimiter=';')

    next(reader, None)  # skip header

    for row in reader:
        if len(row) < 2:
            continue

        code_insee = row[0].strip()
        raw_city = row[1].strip()

        # FILTRE OCCITANIE
        if not any(code_insee.startswith(prefix) for prefix in OCCITANIE_PREFIXES):
            continue

        if raw_city:
            communes.add(normalize_city(raw_city))

# Extraction pour chaque commune
for city in sorted(communes):
    print(f"Extraction OSM pour la ville : {city}")
    out = extract_city_poi(city, config_path, output_dir)
    print(f"Fichier généré : {out}\n")