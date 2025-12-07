import pandas as pd
import requests
import zipfile

data_folder = 'app_data/raw/'

def getCitiesFromInsee():
    
    pop_data_archive = 'DS_POPULATIONS_REFERENCE_CSV_FR.zip'

    url = "https://api.insee.fr/melodi/file/DS_POPULATIONS_REFERENCE/DS_POPULATIONS_REFERENCE_CSV_FR"
    response = requests.get(url)

    with open(data_folder + pop_data_archive, 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile(data_folder + pop_data_archive, 'r') as zip_ref:
        zip_ref.extractall(data_folder)      # this is destination folder 

def get_collected_cities_dict():
    df = pd.read_csv(data_folder+'DS_POPULATIONS_REFERENCE_data.csv', sep=';', header=0)
    print("df :\n", df.head(20))
    return df.head(20).to_dict(orient='records')