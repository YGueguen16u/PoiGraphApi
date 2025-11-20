import requests
import pandas as pd

# input parameters
occitanie_data_file = "dataTourismeOccitanie.csv"
filepath = "data/raw/" + occitanie_data_file

df = pd.read_csv(filepath, sep = ',', index_col = 0)

# basic data exploration
print("first 20 rows of data:", df.head(20))

print("observation number for each variable: \n", df.count())

print("\nvariable types:\n", df.dtypes)

print("\nbasic statistics of quantitative variable:\n", df.describe())

# deduplication  
if df.duplicated().sum() != 0:
    df2 = df.drop_duplicates() 
else:
    df2 = df

df2.duplicated().sum()

# atomic columns extraction 

df2['Code_postal'] = df2['Code_postal_et_commune'].apply(lambda data: data.split('#')[0])
df2['Commune'] = df2['Code_postal_et_commune'].apply(lambda data: data.split('#')[1])
df2.head()

# column selection
df3 = df2.drop(['Code_postal_et_commune', 'Covid19_mesures_specifiques', 'Createur_de_la_donnee', 'SIT_diffuseur'], axis=1)
df3.head()
