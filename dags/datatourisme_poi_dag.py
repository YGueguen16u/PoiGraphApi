from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from src.etl.data_collection.cities.getCitiesInsee import getCitiesFromInsee
from src.etl.data_collection.poi.getDataTourismeCSV import getPoiFromDatatourisme
from src.etl.data_transform.cleanCitiesSpark import get_occitanie_cities
from src.etl.data_transform.cleanDataTourismeSpark import get_poi_datatourisme
from src.etl.data_ingestion.citiesIngestion import ingestCities
from src.etl.data_ingestion.poiIngestion import ingestDatatourismePOI

def test():
    print("connected")

with DAG(
    dag_id="datatourisme_POI_dag",
    schedule_interval=None,
    tags=['POI', 'datatourisme', 'proj_poi'],
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, 1)
    },
    catchup=False
) as my_dag:
    
    test_task = PythonOperator(
        task_id='test_task',
        python_callable=test
    )

    # collect_cities = PythonOperator(
    #     task_id='collect_cities',
    #     python_callable=getCitiesFromInsee
    # )

    # collect_datatourisme_POI = PythonOperator(
    #     task_id='collect_datatourisme_POI',
    #     python_callable=getPoiFromDatatourisme
    # )

    # transform_cities = PythonOperator(
    #     task_id='transform_cities',
    #     python_callable=get_occitanie_cities
    # )

    # transform_datatourisme_POI = PythonOperator(
    #     task_id='transform_datatourisme_POI',
    #     python_callable=get_poi_datatourisme
    # )

    # ingest_cities = PythonOperator(
    #     task_id='ingest_cities',
    #     python_callable=ingestCities
    # )

    # ingest_datatourisme_POI = PythonOperator(
    #     task_id='ingest_datatourisme_POI',
    #     python_callable=ingestDatatourismePOI
    # )

    # collect_cities >> transform_cities >> ingest_cities
    # collect_datatourisme_POI >> transform_datatourisme_POI >> ingest_datatourisme_POI