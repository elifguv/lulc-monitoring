import json
import os
from shapely.geometry import Point, shape

# Each region has its own bbox for correct GPS calculation
REGIONS = {
    "west":   [28.65, 40.00, 29.00, 40.40],
    "center": [29.00, 40.00, 29.25, 40.40],
    "east":   [29.25, 40.00, 29.60, 40.40],
}

def load_districts(geojson_file):
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    districts = []
    for feature in geojson_data['features']:
        name = feature['properties'].get('name')
        if not name:
            continue
        geom = shape(feature['geometry'])
        districts.append({"name": name, "polygon": geom})
    return districts

def process_region_tiles(tiles, region_name, districts):
    """Calculate GPS coordinates and assign districts for one region's tiles."""
    bbox = REGIONS[region_name]
    min_lon, min_lat, max_lon, max_lat = bbox

    # Find grid dimensions for this region only
    region_tiles = [t for t in tiles if t["region"] == region_name]
    if not region_tiles:
        return []

    max_row = max(t["row"] for t in region_tiles)
    max_col = max(t["col"] for t in region_tiles)

    lon_step = (max_lon - min_lon) / (max_col + 1)
    lat_step = (max_lat - min_lat) / (max_row + 1)

    for tile in region_tiles:
        tile_lon = min_lon + (tile["col"] * lon_step) + (lon_step / 2)
        tile_lat = max_lat - (tile["row"] * lat_step) - (lat_step / 2)
        point = Point(tile_lon, tile_lat)

        assigned_district = "Out of Bounds"
        for district in districts:
            if district["polygon"].contains(point):
                assigned_district = district["name"]
                break

        tile["district"] = assigned_district
        tile["lon"] = round(tile_lon, 6)
        tile["lat"] = round(tile_lat, 6)

    return region_tiles

def add_districts_to_json(input_json, output_json, geojson_file):
    print(f"\nProcessing {input_json}...")

    with open(input_json, 'r') as f:
        data = json.load(f)

    districts = load_districts(geojson_file)
    all_enriched_tiles = []

    for region_name in REGIONS:
        enriched = process_region_tiles(data["tiles"], region_name, districts)
        print(f"  {region_name}: {len(enriched)} tiles processed")
        all_enriched_tiles.extend(enriched)

    result = {"tiles": all_enriched_tiles}
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Finished! {len(all_enriched_tiles)} total tiles saved to {output_json}")

if __name__ == "__main__":
    if not os.path.exists("bursa_districts.geojson"):
        print("Error: bursa_districts.geojson not found.")
    else:
        add_districts_to_json(
            "classification_2020.json",
            "classification_2020_enriched.json",
            "bursa_districts.geojson"
        )
        add_districts_to_json(
            "classification_2025.json",
            "classification_2025_enriched.json",
            "bursa_districts.geojson"
        )