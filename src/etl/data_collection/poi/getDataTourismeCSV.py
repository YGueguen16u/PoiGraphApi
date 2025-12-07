import requests
import pandas as pd

data_folder = 'app_data/raw/'
occitanie_data_file = "dataTourismeOccitanie.csv"


def getPoiFromDatatourisme():
    url = "https://static.data.gouv.fr/resources/datatourisme-la-base-nationale-des-donnees-publiques-dinformation-touristique-en-open-data/20251015-025956/datatourisme-reg-occ.csv"
    
    filepath = data_folder + occitanie_data_file

    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

def get_collected_datatourisme_poi_json():
    df = pd.read_csv(data_folder+occitanie_data_file, header=0)
    print("df :\n", df.head(20))
    return df.head(20).to_json(force_ascii=False, orient='records', lines=True)