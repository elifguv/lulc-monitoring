import os
import re
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuration
MODEL_PATH = "bursa_resnet50_sgd_final.keras"
CLASS_NAMES = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake"
]

def classify_city(folder_path, output_json, model):
    print(f"\nStarting AI classification for {folder_path}...")

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Load .png files 
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.png')]  
    )
    
    if len(image_files) == 0:
        print(f"No images found in {folder_path}")
        return

    batch_images = []
    tile_metadata = []

    print(f"Loading {len(image_files)} tiles into memory...")

    for filename in image_files:
        # Extract row and col from filename 
        match = re.search(r'row(\d+)_col(\d+)', filename)
        if not match:
            continue
        
        row, col = int(match.group(1)), int(match.group(2))

        # Load the image and convert to a numpy array
        img_path = os.path.join(folder_path, filename)
        img = load_img(img_path, target_size=(64, 64))
        img_array = img_to_array(img)    

        batch_images.append(img_array)
        tile_metadata.append({"row": row, "col": col, "filename": filename})

    # Convert the python list to a NumPy tensor
    batch_tensor = np.array(batch_images)

    print("Running ResNet50 predictions...")
    # Predict the entire city in one shot
    predictions = model.predict(batch_tensor, batch_size=32)

    results_dict = {"tiles": []}

    for i, pred_array in enumerate(predictions):
        # Get the index of the highest probability
        predicted_class_index = np.argmax(pred_array)
        confidence = float(pred_array[predicted_class_index])
        predicted_label = CLASS_NAMES[predicted_class_index]

        # Attach the prediction to the tile's metadata
        tile_data = tile_metadata[i]
        tile_data["predicted_class"] = predicted_label
        tile_data["confidence"] = round(confidence * 100, 2)
        results_dict["tiles"].append(tile_data)

    # Save to a static JSON file
    with open(output_json, 'w') as f:
        json.dump(results_dict, f, indent=4)

    print(f"Classification complete! Results saved to {output_json}")

# Execution
if __name__ == "__main__":
    print("Loading ResNet-50 AI Model...")
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}. Please check the filename.")
    else:
        resnet_model = load_model(MODEL_PATH)
        print("Model loaded successfully!")

        classify_city('bursa_tiles_2020', 'classification_2020.json', resnet_model)
        classify_city('bursa_tiles_2025', 'classification_2025.json', resnet_model)