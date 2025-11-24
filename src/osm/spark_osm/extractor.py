# extractor.py
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import requests
import json
import os
import time

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

def extract_city_poi(city: str, config_path: str, output_dir: str):
    spark = SparkSession.builder \
        .appName(f"OSM_POI_Extraction_{city}") \
        .master("local[*]") \
        .getOrCreate()

    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    with open(config_path, "r", encoding="utf-8") as f:
        json_file = json.load(f)

    # Build queries
    queries = []
    for main_cat, groups in json_file.items():
        for thematic_group, subcats in groups.items():
            for subcat in subcats:
                query = f"""
                [out:json][timeout:{90}];
                area["name"="{city}"]->.a;
                node["{main_cat}"="{subcat}"](area.a);
                out center;
                """
                queries.append({
                    "main_cat": main_cat,
                    "thematic_group": thematic_group,
                    "subcat": subcat,
                    "query": query
                })

    # Fetch function for workers
    def fetch_overpass(record):
        for attempt in range(3):
            try:
                res = requests.post(
                    OVERPASS_URL,
                    data={"data": record["query"]},
                    headers={"User-Agent": "PoiGraphApi-Spark/1.0"},
                    timeout=90
                )
                if res.status_code != 200 or not res.text.strip():
                    time.sleep(1 + attempt)
                    continue

                js = res.json()
                results = []
                for e in js.get("elements", []):
                    tags = e.get("tags", {})
                    results.append({
                        "main_cat": record["main_cat"],
                        "thematic_group": record["thematic_group"],
                        "subcat": record["subcat"],
                        "name": tags.get("name"),
                        "lat": e.get("lat"),
                        "lon": e.get("lon")
                    })
                return results
            except Exception:
                time.sleep(1 + attempt)
        return []

    # Run Spark parallelism
    rdd_queries = sc.parallelize(queries, 8)
    rdd_results = rdd_queries.flatMap(fetch_overpass).collect()

    # 4. Convert to Spark DataFrame
    schema = StructType([
        StructField("main_cat", StringType()),
        StructField("thematic_group", StringType()),
        StructField("subcat", StringType()),
        StructField("name", StringType()),
        StructField("lat", FloatType()),
        StructField("lon", FloatType())
    ])

    df = spark.createDataFrame(rdd_results, schema=schema)

    # Convert JSON hierarchical format (your original output)
    data = {}
    for r in rdd_results:
        data \
            .setdefault(r["main_cat"], {}) \
            .setdefault(r["thematic_group"], {}) \
            .setdefault(r["subcat"], []) \
            .append({
                "name": r["name"],
                "lat": r["lat"],
                "lon": r["lon"]
            })

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{city.lower()}_poi_spark.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return df, output_path