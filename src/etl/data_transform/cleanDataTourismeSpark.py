from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.conf import SparkConf
from pyspark import SparkContext
from src.utils.checkMissingValues import getMissingValues, missingTable

def cleanDataTourismePOI():
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

    ### open existing datafile ensuring accurate data types
    data_folder = 'app_data/raw/'
    occitanie_data_file = data_folder + 'dataTourismeOccitanie.csv'

    data_tourisme_schema = StructType([StructField("Nom_du_POI", StringType()),\
                        StructField("Categories_de_POI", StringType()),\
                        StructField("Latitude", FloatType()),\
                        StructField("Longitude", FloatType()),\
                        StructField("Adresse_postale", StringType()),\
                        StructField("Code_postal_et_commune", StringType()),\
                        StructField("Periodes_regroupees", StringType()),\
                        StructField("Covid19_mesures_specifiques", StringType()),\
                        StructField("Createur_de_la_donnee", StringType()),\
                        StructField("SIT_diffuseur", StringType()),\
                        StructField("Date_de_mise_a_jour", DateType()),\
                        StructField("Contacts_du_POI", StringType()),\
                        StructField("Classements_du_POI", StringType()),\
                        StructField("Description", StringType()),\
                        StructField("URI_ID_du_POI", StringType())
                        ])

    df = spark.read.schema(data_tourisme_schema)\
                .option("delimiter", ",")\
                .option("header", True)\
                .option("multiline", True)\
                .option("escape", "\"")\
                .csv(occitanie_data_file)



    ### columns selection
    df_select = df.drop(*[
        'Periodes_regroupees',
        'Covid19_mesures_specifiques',
        'Createur_de_la_donnee',
        'SIT_diffuseur',
        'Classements_du_POI',
        'URI_ID_du_POI'])

    ### columns split

    # first, split 'Code_postal_et_commune' in two atomic parts, clean 'Code_postal' and cast it to 'int'
    df_split = df_select.withColumn('Code_postal', split(df_select['Code_postal_et_commune'], '#')[0])\
        .withColumn('Commune', split(df_select['Code_postal_et_commune'], '#')[1])
    df_split = df_split.drop('Code_postal_et_commune')
    df_split = df_split.withColumn('Code_postal', regexp_replace(df_split['Code_postal'], ' ',''))
    df_split = df_split.withColumn('Code_postal', df_split['Code_postal'])

    # maenwhile, select only postal code corresponding to montpellier
    df_split_mtp = df_split.where((col('Code_postal') >= 34000) & (col('Code_postal') < 34100))

    # second, split 'Categories_de_POI' into 2 (for montpellier) or 3 categories (for whole occitanie) 
    # Montpellier case
    df_split_2 = df_split_mtp.withColumn('Cat_POI_first_init', split(df_split_mtp['Categories_de_POI'], '#')[1])\
        .withColumn('Cat_POI_second_init', split(df_split_mtp['Categories_de_POI'], '#')[2])

    df_split_3 = df_split_2.withColumn('Categories_de_POI_niveau1', split(df_split_2['Cat_POI_first_init'], '\|')[0])\
        .withColumn('Categories_de_POI_niveau2', split(df_split_2['Cat_POI_second_init'], '\|')[0])
    # df_split_3.select(['Categories_de_POI_niveau1', 'Categories_de_POI_niveau2']).show(5)
    df_split_3 = df_split_3.drop(*['Categories_de_POI', 'Cat_POI_first_init', 'Cat_POI_second_init'])


    # Occitanie case, uncomment when ready
    # df_split_2 = df_split.withColumn('Cat_POI_first_init', split(df_split['Categories_de_POI'], '#')[1])\
    #     .withColumn('Cat_POI_second_init', split(df_split['Categories_de_POI'], '#')[2])\
    #     .withColumn('Cat_POI_third_init', split(df_split['Categories_de_POI'], '#')[3])

    # df_split_3 = df_split_2.withColumn('Categories_de_POI_niveau1', split(df_split_2['Cat_POI_first_init'], '\|')[0])\
    #     .withColumn('Categories_de_POI_niveau2', split(df_split_2['Cat_POI_second_init'], '\|')[0])\
    #     .withColumn('Categories_de_POI_niveau3', split(df_split_2['Cat_POI_third_init'], '\|')[0])
    # df_split_3.select(['Categories_de_POI_niveau1', 'Categories_de_POI_niveau2', 'Categories_de_POI_niveau3']).show(5)
    # df_split_3 = df_split_3.drop(*['Categories_de_POI', 'Cat_POI_first_init', 'Cat_POI_second_init', 'Cat_POI_third_init'])

    ### columns cleaning
    df_clean = df_split_3.withColumn('Nom_du_POI', lower(df_split_3['Nom_du_POI']))\
        .withColumn('Contacts_du_POI', regexp_replace('Contacts_du_POI', '#', ''))\
        .withColumn('Latitude', round(df_split_3['Latitude'], 6))\
        .withColumn('Longitude', round(df_split_3['Longitude'], 6))

    ### deduplication according to POI_name, latitude and longitude 

    #for checking purpose only
    def return_duplicates(df):
      return(df.groupBy(df.columns).agg(count("*").alias("duplicates")).filter(col("duplicates") >= 2))

    print("----------  number of values in dataset :\n")
    print(df_clean.count())

    print("----------  number of duplicates in dataset :\n")
    print(return_duplicates(df_clean).sort("duplicates", ascending=False).count())
    # return_duplicates(df_clean).sort("duplicates", ascending=False).show(10)
    

    df_unique = df_clean.dropDuplicates(['Nom_du_POI', 'Latitude', 'Longitude'])

    print("----------  number of Nas and null values :\n")
    missingTable(getMissingValues(df_unique))

    df_unique.write.mode("overwrite").csv("app_data/cleaned_data/poi_datatourisme_clean.csv", header= True, sep=',')

    return df_unique

def get_poi_datatourisme():
    return cleanDataTourismePOI()

def get_poi_datatourisme_dict():
    return cleanDataTourismePOI().toPandas().to_dict(orient='records')

