import asyncio
import requests
import json
import os
import time

# Config 
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"
CITY = "Montpellier"
MAX_CONCURRENT = 8  # parallel limit

# Load subcategories
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "annexe", "sub_categories.json")
with open(config_path, "r", encoding="utf-8") as f:
    json_file = json.load(f)

data = {}

# Fetch function (synchronous)
def fetch_osm_sync(main_cat, thematic_group, subcat, query):
    try:
        res = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers={"User-Agent": "PoiGraphApi/1.0"},
            timeout=90
        )
        if res.status_code != 200:
            return f"{main_cat}={subcat}: HTTP {res.status_code}"

        js = res.json()
        elements = js.get("elements", [])
        for e in elements:
            tags = e.get("tags", {})
            name = tags.get("name")
            lat, lon = e.get("lat"), e.get("lon")
            data \
                .setdefault(main_cat, {}) \
                .setdefault(thematic_group, {}) \
                .setdefault(subcat, []) \
                .append({"name": name, "lat": lat, "lon": lon})

        return f"{main_cat}={subcat} → {len(elements)} results"
    except Exception as err:
        return f"{main_cat}={subcat} failed: {err}"

# Async wrapper around sync requests
async def fetch_osm_async(sem, main_cat, thematic_group, subcat, query):
    async with sem:
        # Run blocking I/O inside thread pool
        return await asyncio.to_thread(fetch_osm_sync, main_cat, thematic_group, subcat, query)

# Main async routine
async def main():
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = []

    for main_cat, groups in json_file.items():
        for thematic_group, subcats in groups.items():
            for subcat in subcats:
                q = f"""
                [out:json][timeout:60];
                area["name"="{CITY}"]->.a;
                node["{main_cat}"="{subcat}"](area.a);
                out center;
                """
                tasks.append(fetch_osm_async(sem, main_cat, thematic_group, subcat, q))

    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)

# Run
start = time.time()
print(f"Fetching POIs for {CITY} ...")

asyncio.run(main())

# Save
out_path = f"{CITY.lower()}_poi.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = sum(len(p) for m in data.values() for g in m.values() for p in g.values())
print(f"\n{total} POIs saved in {out_path}")
print(f"Completed in {time.time() - start:.1f}s")