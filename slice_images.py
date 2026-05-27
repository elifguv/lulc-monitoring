import cv2
import os
import numpy as np
from patchify import patchify

def slice_city_map(input_folder, output_folder, tile_size=64):
    print(f"\nStarting slicing operation for: {input_folder}")
    
    # Find the downloaded image
    image_path = None
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".png"):
                image_path = os.path.join(root, file)
                break
        if image_path: 
            break
            
    if not image_path:
        print(f"Could not find a PNG image anywhere in {input_folder}")
        return

    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert images to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Crop the image so it's divisible by the tile size
    height = (image.shape[0] // tile_size) * tile_size
    width = (image.shape[1] // tile_size) * tile_size
    image = image[:height, :width]
    
    print(f"Cropped map dimensions: {height}x{width}")

    # Create the output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Slice the image into a 64x64 grid with no overlapping
    patches = patchify(image, (tile_size, tile_size, 3), step=tile_size)
    
    tile_count = 0
    
    # Extract and save each individual tile
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            # Extract the 3D block (64, 64, 3)
            single_patch = patches[i, j, 0]
            
            save_patch = cv2.cvtColor(single_patch, cv2.COLOR_RGB2BGR)
            
            # Name the file with its exact row and column position
            tile_name = f"tile_row{i:03d}_col{j:03d}.png"
            cv2.imwrite(os.path.join(output_folder, tile_name), save_patch)
            tile_count += 1

    print(f"Slicing complete! {tile_count} tiles saved to '{output_folder}'")

# Execute the slicing
if __name__ == "__main__":
    if os.path.exists('bursa_raw_data_2020'):
        slice_city_map('bursa_raw_data_2020', 'bursa_tiles_2020')
        
    if os.path.exists('bursa_raw_data_2025'):
        slice_city_map('bursa_raw_data_2025', 'bursa_tiles_2025')