import os
import re
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Configuration
MODEL_PATH = "bursa_resnet50_sgd_final.keras"
CLASS_NAMES = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake"
]

def classify_city(folder_path, output_json, model):
    print(f"\nStarting classification for {folder_path}...")

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Load images
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.png')]
    )

    if len(image_files) == 0:
        print(f"No PNG tiles found in {folder_path}")
        return

    batch_images = []
    tile_metadata = []

    print(f"Loading {len(image_files)} tiles...")

    for filename in image_files:
        # Regex to capture region prefix + row + col 
        match = re.search(r'(\w+)_tile_row(\d+)_col(\d+)', filename)
        if not match:
            continue
        region = match.group(1)
        row = int(match.group(2))
        col = int(match.group(3))

        img_path = os.path.join(folder_path, filename)
        img = load_img(img_path, target_size=(64, 64))
        img_array = img_to_array(img)
        batch_images.append(img_array)
        tile_metadata.append({
            "region": region,
            "row": row,
            "col": col,
            "filename": filename
        })

    batch_tensor = np.array(batch_images)
    print(f"Running ResNet50 predictions on {len(batch_images)} tiles...")

    predictions = model.predict(batch_tensor, batch_size=32)
    results_dict = {"tiles": []}

    for i, pred_array in enumerate(predictions):
        # Get the index of the highest probability
        predicted_class_index = np.argmax(pred_array)
        confidence = float(pred_array[predicted_class_index])
        predicted_label = CLASS_NAMES[predicted_class_index]

        tile_data = tile_metadata[i]
        tile_data["predicted_class"] = predicted_label
        tile_data["confidence"] = round(confidence * 100, 2)
        results_dict["tiles"].append(tile_data)

    with open(output_json, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print(f"Classification complete! Results saved to {output_json}")

if __name__ == "__main__":
    print("Loading ResNet-50 model...")
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}")
    else:
        resnet_model = load_model(MODEL_PATH)
        print("Model loaded successfully!")
        classify_city('bursa_tiles_2020', 'classification_2020.json', resnet_model)
        classify_city('bursa_tiles_2025', 'classification_2025.json', resnet_model)