import pandas as pd

# Charger le CSV
df = pd.read_csv("poi_profile_matrix.csv")

print("=== Aperçu du fichier ===")
print(df.head(), "\n")

print("=== Info colonnes ===")
print(df.info(), "\n")

# Conversion automatique en float (sauf la colonne des profils)
for col in df.columns:
    if col != "profile_type":
        df[col] = df[col].astype(float)

print("=== Vérification des types ===")
print(df.dtypes)