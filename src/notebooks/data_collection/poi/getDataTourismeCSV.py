import requests
import pandas as pd

# input parameters
url = "https://static.data.gouv.fr/resources/datatourisme-la-base-nationale-des-donnees-publiques-dinformation-touristique-en-open-data/20251015-025956/datatourisme-reg-occ.csv"
occitanie_data_file = "dataTourismeOccitanie.csv"

filepath = "work/data/raw/" + occitanie_data_file

response = requests.get(url)
with open(filepath, 'wb') as f:
    f.write(response.content)

