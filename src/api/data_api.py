from fastapi import FastAPI, Depends
from src.api.auth import authenticate_user 
from src.etl.data_collection.poi.getDataTourismeCSV import get_collected_datatourisme_poi_json
from src.etl.data_collection.cities.getCitiesInsee import get_collected_cities_dict
from src.etl.data_transform.cleanCitiesSpark import get_occitanie_cities_dict
from src.etl.data_transform.cleanDataTourismeSpark import get_poi_datatourisme_dict
from src.utils.getSecrets import _get_secret
import snowflake.connector 
 

# from snowflake.snowpark import Session
# from snowflake.core import Root

app = FastAPI(title="data POI project", version="1.0.0")

@app.get("/data")
async def home():
    ''' HOME URL (unprotected)
    '''
    return {"message": "Welcome to data API of POI project"}


### ETL Data API

@app.get("/data/collect/poi/datatourisme")
async def get_collected_poi_datatourisme(current_user: str = Depends(authenticate_user)):
    ''' allow to retrieve poi data from datatourisme database as they are collected 
    from DataTourisme website (protected URL)
    '''
    return get_collected_datatourisme_poi_json()

@app.get("/data/transform/poi/datatourisme")
async def get_transformed_poi_datatourisme(current_user: str = Depends(authenticate_user)):
    ''' allow to retrieve poi data from datatourisme database after ETL operations 
        have been performed (protected URL)
    '''
    return get_poi_datatourisme_dict()


@app.get("/data/collect/cities")
async def get_collected_cities(current_user: str = Depends(authenticate_user)):
    ''' allow to retrieve city data from Insee database as they are collected 
    from INSEE website (protected URL)
    '''
    return get_collected_cities_dict()

@app.get("/data/transform/cities")
async def get_transformed_cities(current_user: str = Depends(authenticate_user)):
    ''' allow to retrieve city data from Insee database after ETL operations 
        have been performed (protected URL)
    '''
    return get_occitanie_cities_dict()


### Snowflake Data API
warehouse_name = 'POI_CONNECTOR_OPS_WH'
database_name = 'POI_POSTGRES_RAW'
schema_name = 'SCHEMA_POI'

# See if needed

# connection_parameters = dict(
#     user=_get_secret("snowflake_user"),
#     password=_get_secret("snowflake_secret"),
#     account=_get_secret("snowflake_account"),
#     warehouse = warehouse_name,
#     database = database_name,
#     schema = schema_name
#     # role = 'role if needed'
# )

# session = Session.builder.configs(connection_parameters).create()

# conn = snowflake.connector.connect(
#     user=_get_secret("snowflake_user"),
#     password=_get_secret("snowflake_secret"),
#     account=_get_secret("snowflake_account"),
#     warehouse = warehouse_name,
#     database = database_name,
#     schema = schema_name,
#     role = 'ACCOUNTADMIN'
#     )

# cursor = conn.cursor()

# cursor.execute("SELECT * FROM POI")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


# conn.close()