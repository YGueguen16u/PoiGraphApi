import pandas as pd
import requests
import zipfile

data_folder = 'app_data/raw/'
pop_data_archive = 'DS_POPULATIONS_REFERENCE_CSV_FR.zip'

url = "https://api.insee.fr/melodi/file/DS_POPULATIONS_REFERENCE/DS_POPULATIONS_REFERENCE_CSV_FR"
response = requests.get(url)

with open(data_folder + pop_data_archive, 'wb') as f:
    f.write(response.content)

with zipfile.ZipFile(data_folder + pop_data_archive, 'r') as zip_ref:
    zip_ref.extractall(data_folder)      # this is destination folder 

