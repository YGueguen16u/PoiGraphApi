# src/notebooks/data_ingestion/profile_ingestion.py

import sys, os
from pyspark.sql import SparkSession, Row
from pyspark.conf import SparkConf
from pyspark import SparkContext
from datetime import datetime
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)  

from src.user_generator import RandomUserGenerator
from src.user_generator.src.utils.pg_lookup import get_category_id

# Spark init
conf = SparkConf()
conf.set("spark.log.level", "error")
conf.set("spark.ui.showConsoleProgress", "false")
sc = SparkContext.getOrCreate(conf=conf)

spark = SparkSession\
        .builder\
        .config("spark.jars", "/usr/local/spark/jars/postgresql-42.7.8.jar")\
        .appName("projet_User")\
        .master("local[*]")\
        .getOrCreate()

def write_to_postgres(df, table_name):
    df.write \
      .mode("append") \
      .format("jdbc") \
      .option("url", "jdbc:postgresql://pg_db:5432/poi_db") \
      .option("dbtable", table_name) \
      .option("user", "postgres") \
      .option("password", "postgres") \
      .save()

# Generate user
gen = RandomUserGenerator(
    names_path="src/user-generator/data/names.json",
    categories_path="src/user-generator/data/category_poi.json",
    poi_matrix_path="src/user-generator/data/poi_profile_matrix.csv",
)

user = gen.generate_user()

# Insert User_profile
profile_id = str(uuid.uuid4())

df_profile = spark.createDataFrame([
    Row(
        user_profile_id = profile_id,
        category_id = None,
        max_distance = user.profile.max_distance,
        transport_mean = user.profile.transport_mean
    )
])
write_to_postgres(df_profile, "user_profile")

# Insert User
user_id = str(uuid.uuid4())

df_user = spark.createDataFrame([
    Row(
        user_id = user_id,
        user_profile_id = profile_id,
        user_name = f"{user.first_name} {user.last_name}",
        date_creation = datetime.utcnow(),
        long = user.Longitude,
        lat = user.Latitude
    )
])
write_to_postgres(df_user, "user")

# Insert POI preferences
rows = []
for poi in user.profile.poi_preferences:
    cat_id = get_category_id(poi)
    if cat_id:
        rows.append(
            Row(
                category_user_profile_id = str(uuid.uuid4()),
                category_id = cat_id,
                user_profile_id = profile_id
            )
        )

df_cup = spark.createDataFrame(rows)
write_to_postgres(df_cup, "category_user_profile")