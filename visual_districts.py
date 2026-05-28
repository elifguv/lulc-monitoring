import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def visualize_districts(json_file):
    print(f"Verifying geographic borders for {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    max_row = max([tile["row"] for tile in data["tiles"]])
    max_col = max([tile["col"] for tile in data["tiles"]])
    
    # Find all the unique districts the script assigned
    districts = list(set([tile.get("district", "Unknown") for tile in data["tiles"]]))
    
    # Assign a random distinct color to every district
    np.random.seed(42) # Keep the colors the same on every run
    district_colors = {d: np.random.rand(3,) for d in districts}
    
    # Out of Bounds is pure black so it's obvious
    if "Out of Bounds" in district_colors:
        district_colors["Out of Bounds"] = [0, 0, 0]
        
    grid_map = np.ones((max_row + 1, max_col + 1, 3))
    
    # Paint the canvas based on the district name
    for tile in data["tiles"]:
        r, c = tile["row"], tile["col"]
        dist = tile.get("district", "Out of Bounds")
        grid_map[r, c] = district_colors[dist]
        
    # Plot the map
    plt.figure(figsize=(12, 6))
    plt.imshow(grid_map)
    plt.title('Spatial Join Verification: Bursa Districts', fontsize=16)
    plt.axis('off')
    
    legend_handles = [mpatches.Patch(color=color, label=label) for label, color in district_colors.items()]
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_districts('classification_2020_enriched.json')
    visualize_districts('classification_2025_enriched.json')