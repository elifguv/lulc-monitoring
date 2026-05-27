import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define a specific color for every EuroSAT class by using standard map colors (Forest = Green, Water = Blue, Urban = Red)
CLASS_COLORS = {
    "AnnualCrop": [1.0, 0.84, 0.0],         # Gold
    "Forest": [0.0, 0.5, 0.0],              # Dark Green
    "HerbaceousVegetation": [0.56, 0.93, 0.56], # Light Green
    "Highway": [0.5, 0.5, 0.5],             # Gray
    "Industrial": [0.5, 0.0, 0.5],          # Purple
    "Pasture": [0.6, 0.8, 0.2],             # Yellow-Green
    "PermanentCrop": [1.0, 0.65, 0.0],      # Orange
    "Residential": [1.0, 0.0, 0.0],         # Red
    "River": [0.0, 1.0, 1.0],               # Cyan
    "SeaLake": [0.0, 0.0, 1.0]              # Blue
}

def generate_classification_map(json_file, title):
    print(f"Generating visual map for {json_file}...")
    
    # Load the JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Figure out the grid size by finding the highest row and column numbers
    max_row = max([tile["row"] for tile in data["tiles"]])
    max_col = max([tile["col"] for tile in data["tiles"]])
    
    grid_map = np.ones((max_row + 1, max_col + 1, 3))
    
    # Paint the canvas based on the AI's predictions
    for tile in data["tiles"]:
        r, c = tile["row"], tile["col"]
        prediction = tile["predicted_class"]
        
        # Look up the color, default to black if something goes wrong
        grid_map[r, c] = CLASS_COLORS.get(prediction, [0, 0, 0])
        
    # Plot the result
    plt.figure(figsize=(12, 6))
    plt.imshow(grid_map)
    plt.title(title, fontsize=16)
    plt.axis('off')

    legend_handles = [
        mpatches.Patch(color=color, label=label) 
        for label, color in CLASS_COLORS.items()
    ]
    # Put the legend outside the map box
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_classification_map('classification_2025.json', 'Bursa LULC Classification - 2025')