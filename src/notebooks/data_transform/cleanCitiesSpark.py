from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.conf import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.set("spark.log.level", "error") # To display only errors
conf.set("spark.ui.showConsoleProgress", "false") # To display only Spark jobs progression in Python

### definition of SparkContext
sc = SparkContext.getOrCreate(conf=conf) 

spark = SparkSession\
        .builder\
        .appName("projet_POI")\
        .master("local[*]")\
        .getOrCreate()

### open existing datafile 

data_folder = 'work/'
pop_france_data = data_folder+'DS_POPULATIONS_REFERENCE_data.csv'
df = spark.read.option("inferSchema", True)\
               .option("delimiter", ";")\
               .option("header", True)\
               .csv(pop_france_data)


### columns selection
# we want pop details at city level and for the year 2022
df_select = df.where((col('GEO_OBJECT') == 'COM')& (col('TIME_PERIOD') == 2022))
df_select = df_select.drop(*[
    'GEO_OBJECT',
    'FREQ'])

### row split for montpellier and occitanie

df_mtp = df_select.where((col('POPREF_MEASURE') == 'PTOT') & (col('GEO') == '34172'))

# Occitanie case, uncomment when ready
df_occitanie = df_select.where((col('POPREF_MEASURE') == 'PTOT') & (
                               (col('GEO') >= '09000') & (col('GEO') < '10000')| 
                               (col('GEO') >= '11000') & (col('GEO') < '13000')| 
                               (col('GEO') >= '30000') & (col('GEO') < '33000')| 
                               (col('GEO') >= '34000') & (col('GEO') < '35000')| 
                               (col('GEO') >= '46000') & (col('GEO') < '47000')| 
                               (col('GEO') >= '48000') & (col('GEO') < '49000')| 
                               (col('GEO') >= '65000') & (col('GEO') < '67000')| 
                               (col('GEO') >= '81000') & (col('GEO') < '83000'))
                              )

### columns cleaning
df_occitanie_clean = df_occitanie.withColumn('Annee_Maj', df_occitanie['TIME_PERIOD'].cast("int"))
df_occitanie_clean = df_occitanie_clean.withColumnRenamed('GEO','Code_commune_INSEE')\
                                       .withColumnRenamed('OBS_VALUE','Population')
df_occitanie_clean = df_occitanie_clean.drop(*[
    'GEO_OBJECT',
    'POPREF_MEASURE',
    'TIME_PERIOD'])

# get and clean code conversion between postal_code and insee_code

codes_schema = StructType([StructField("Code_commune_INSEE", StringType()),\
                    StructField("Nom_de_la_commune", StringType()),\
                    StructField("Code_postal", StringType()),\
                    StructField("Libell�_d_acheminement", StringType()),\
                    StructField("Ligne_5", StringType())
                    ])

codes = spark.read.schema(codes_schema)\
               .option("delimiter", ";")\
               .option("header", True)\
               .csv(data_folder+'019HexaSmal.csv')
codes = codes.drop(*[
    'Libell�_d_acheminement',
    'Ligne_5'])
codes = codes.withColumnRenamed('#Code_commune_INSEE','Code_commune_INSEE')

# clean nom commune : lowercase no whitespace
codes_clean = codes.withColumn('Nom_de_la_commune',lower(regexp_replace(codes['Nom_de_la_commune'], ' ','_')))
# drop duplicates
codes_clean = codes_clean.dropDuplicates(['Code_commune_INSEE'])

# innerjoin between occitanie file and codes file
occitanie_cities = df_occitanie_clean.join(codes_clean, on=['Code_commune_INSEE'], how='inner')

