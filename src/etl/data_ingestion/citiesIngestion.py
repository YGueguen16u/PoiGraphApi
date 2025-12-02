# src/notebooks/data_ingestion/citiesIngestion.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.conf import SparkConf
from pyspark import SparkContext
from etl.data_transform.cleanCitiesSpark import get_occitanie_cities


def ingestCities():
        conf = SparkConf()
        conf.set("spark.log.level", "error") # To display only errors
        conf.set("spark.ui.showConsoleProgress", "false") # To display only Spark jobs progression in Python

        ### definition of SparkContext
        sc = SparkContext.getOrCreate(conf=conf) 

        spark = SparkSession\
                .builder\
                .config("spark.jars", "/usr/local/spark/jars/postgresql-42.7.8.jar")\
                .appName("projet_POI")\
                .master("local[*]")\
                .getOrCreate()

        occitanie_cities = get_occitanie_cities()

        occitanie_cities.write \
        .mode('overwrite') \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://pg_db:5432/poi_db") \
        .option("dbtable", "city") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .save()
