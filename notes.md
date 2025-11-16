docker run --rm -it \
  -v $(pwd)/src:/app/src \
  spark-poigraph \
  python3 /app/src/osm_extract_spark.py