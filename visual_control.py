import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CLASS_COLORS = {
    "AnnualCrop": [1.0, 0.84, 0.0],
    "Forest": [0.0, 0.5, 0.0],
    "HerbaceousVegetation": [0.56, 0.93, 0.56],
    "Highway": [0.5, 0.5, 0.5],
    "Industrial": [0.5, 0.0, 0.5],
    "Pasture": [0.6, 0.8, 0.2],
    "PermanentCrop": [1.0, 0.65, 0.0],
    "Residential": [1.0, 0.0, 0.0],
    "River": [0.0, 1.0, 1.0],
    "SeaLake": [0.0, 0.0, 1.0]
}

REGION_ORDER = ["west", "center", "east"]

def generate_classification_map(json_file, title):
    print(f"Generating visual map for {json_file}...")

    with open(json_file, 'r') as f:
        data = json.load(f)

    # Group tiles by region
    regions = {}
    for tile in data["tiles"]:
        region = tile.get("region", "unknown")
        if region not in regions:
            regions[region] = []
        regions[region].append(tile)

    # Build a grid per region then concatenate horizontally
    region_grids = []
    for region_name in REGION_ORDER:
        if region_name not in regions:
            continue
        tiles = regions[region_name]
        max_row = max(t["row"] for t in tiles)
        max_col = max(t["col"] for t in tiles)

        # White canvas for this region
        grid = np.ones((max_row + 1, max_col + 1, 3))

        for tile in tiles:
            r, c = tile["row"], tile["col"]
            prediction = tile["predicted_class"]
            grid[r, c] = CLASS_COLORS.get(prediction, [0, 0, 0])

        region_grids.append(grid)

    if not region_grids:
        print("No region data found.")
        return

    # Make all grids the same height before concatenating
    max_height = max(g.shape[0] for g in region_grids)
    padded_grids = []
    for g in region_grids:
        if g.shape[0] < max_height:
            # Pad bottom with white
            pad = np.ones((max_height - g.shape[0], g.shape[1], 3))
            g = np.concatenate([g, pad], axis=0)
        padded_grids.append(g)

    # Concatenate west | center | east side by side
    full_map = np.concatenate(padded_grids, axis=1)

    plt.figure(figsize=(18, 6))
    plt.imshow(full_map)
    plt.title(title, fontsize=16)
    plt.axis('off')

    legend_handles = [
        mpatches.Patch(color=color, label=label)
        for label, color in CLASS_COLORS.items()
    ]
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_classification_map('classification_2020.json', 'Bursa LULC Classification - 2020')
    generate_classification_map('classification_2025.json', 'Bursa LULC Classification - 2025')