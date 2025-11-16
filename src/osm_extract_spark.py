from pyspark.sql import SparkSession, Row
import requests
import json
import os
import time

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"
CITY = "Montpellier"

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "annexe", "sub_categories.json")

with open(config_path, "r", encoding="utf-8") as f:
    json_file = json.load(f)

spark = SparkSession.builder \
    .appName("OSM_POI_Extraction") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

# Build queries
queries = []
for main_cat, groups in json_file.items():
    for thematic_group, subcats in groups.items():
        for subcat in subcats:
            query = f"""
            [out:json][timeout:60];
            area["name"="{CITY}"]->.a;
            node["{main_cat}"="{subcat}"](area.a);
            out center;
            """
            queries.append({
                "main_cat": main_cat,
                "thematic_group": thematic_group,
                "subcat": subcat,
                "query": query
            })

# Function executed in Spark workers
def fetch_overpass(record):
    """Robust HTTP fetch with retry."""
    for attempt in range(3):
        try:
            res = requests.post(
                OVERPASS_URL,
                data={"data": record["query"]},
                headers={"User-Agent": "PoiGraphApi-Spark/1.0"},
                timeout=90
            )

            # Some Overpass nodes return empty body under load → retry
            if res.status_code != 200 or not res.text.strip():
                time.sleep(1 + attempt)
                continue

            js = res.json()
            elements = js.get("elements", [])

            results = []
            for e in elements:
                tags = e.get("tags", {})
                name = tags.get("name")
                lat, lon = e.get("lat"), e.get("lon")
                results.append({
                    "main_cat": record["main_cat"],
                    "thematic_group": record["thematic_group"],
                    "subcat": record["subcat"],
                    "name": name,
                    "lat": lat,
                    "lon": lon
                })
            return results

        except Exception:
            time.sleep(1 + attempt)

    # After 3 failed attempts
    print(f"[ERROR] {record['main_cat']}={record['subcat']} → FAILED AFTER 3 RETRIES")
    return []

# Run Spark
start = time.time()
print(f"Fetching POIs for {CITY} using Spark...")

MAX_CONCURRENT = 8
rdd_queries = sc.parallelize(queries, MAX_CONCURRENT)
rdd_results = rdd_queries.flatMap(fetch_overpass).collect()


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

# Save JSON identique à asyncio
output_dir = os.path.join(script_dir, "output")
os.makedirs(output_dir, exist_ok=True) 

output_path = os.path.join(output_dir, f"{CITY.lower()}_poi_spark.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count results the same way as asyncio code
total = sum(len(p) for m in data.values() for g in m.values() for p in g.values())
print(f"{total} POIs saved to {output_path}")
print(f"Completed in {time.time() - start:.1f}s")

spark.stop()