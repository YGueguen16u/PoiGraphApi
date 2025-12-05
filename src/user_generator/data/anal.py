# src/user-generator/data/anal.py
import pandas as pd

# Charger le CSV
df = pd.read_csv("src/user-generator/data/poi_profile_matrix.csv", index_col=0)

print("=== Aperçu du fichier ===")
print(df.head(10), "\n")

print("=== Info colonnes ===")
print(df.info(), "\n")

# Convertir toutes les colonnes en float
df = df.astype(float)

print("=== DataFrame converti ===")
print(df.head(10))