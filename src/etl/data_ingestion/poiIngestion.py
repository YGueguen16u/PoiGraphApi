from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.conf import SparkConf
from pyspark import SparkContext
from etl.data_transform.cleanDataTourismeSpark import get_poi_datatourisme

def ingestDatatourismePOI():
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

        poi_datatourisme = get_poi_datatourisme()

        poi_datatourisme.write \
        .mode('overwrite') \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://pg_db:5432/poi_db") \
        .option("dbtable", "poi") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .save()
