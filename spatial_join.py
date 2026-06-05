import json
import os
from shapely.geometry import Point, shape

# Configuration
BBOX = [28.75, 40.10, 29.25, 40.35] # [min_lon, min_lat, max_lon, max_lat]
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = BBOX

def add_districts_to_json(input_json, output_json, geojson_file):
    print(f"Processing {input_json}...")

    # Load the AI Classification JSON
    with open(input_json, 'r') as f:
        data = json.load(f)

    # Load the district polygons
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Convert the GeoJSON features into Shapely polygons
    districts = []
    for feature in geojson_data['features']:
        name = feature['properties'].get('name', 'Unknown')
        geom = shape(feature['geometry'])
        districts.append({"name": name, "polygon": geom})

    # Find the size of the grid
    max_row = max(tile["row"] for tile in data["tiles"])
    max_col = max(tile["col"] for tile in data["tiles"])

    # Calculate geographic steps
    lon_step = (MAX_LON - MIN_LON) / (max_col + 1)
    lat_step = (MAX_LAT - MIN_LAT) / (max_row + 1)

    for tile in data["tiles"]:
        # Find the GPS center of the tile
        # Row 0 is the top of the image (Max Lat), moving downwards
        tile_lon = MIN_LON + (tile["col"] * lon_step) + (lon_step / 2)
        tile_lat = MAX_LAT - (tile["row"] * lat_step) - (lat_step / 2)
        
        point = Point(tile_lon, tile_lat)
        assigned_district = "Out of Bounds"

        # Check which district boundary this point falls inside
        for district in districts:
            if district["polygon"].contains(point):
                assigned_district = district["name"]
                break

        # Attach the district to the tile's data
        tile["district"] = assigned_district

    # Save the new enriched JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Finished! Data saved to {output_json}")

if __name__ == "__main__":
    if not os.path.exists("bursa_districts.geojson"):
        print("Error: bursa_districts.geojson not found in folder.")
    else:
        # Run the spatial join for both years
        add_districts_to_json("classification_2020.json", "classification_2020_enriched.json", "bursa_districts.geojson")
        add_districts_to_json("classification_2025.json", "classification_2025_enriched.json", "bursa_districts.geojson")