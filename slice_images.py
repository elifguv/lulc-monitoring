import cv2
import os
import numpy as np
from patchify import patchify

REGIONS = ["west", "center", "east"]

def find_image_in_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".png"):
                return os.path.join(root, file)
    return None

def slice_region(year, region_name, output_folder, tile_size=64):
    input_folder = f'bursa_raw_data_{year}/{region_name}'
    print(f"\nSlicing {region_name} region for {year}...")

    image_path = find_image_in_folder(input_folder)
    if not image_path:
        print(f"  Could not find PNG in {input_folder}")
        return 0

    image = cv2.imread(image_path)
    if image is None:
        print(f"  Failed to load image at {image_path}")
        return 0

    # Convert images to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Crop the image so it's divisible by the tile size
    height = (image.shape[0] // tile_size) * tile_size
    width = (image.shape[1] // tile_size) * tile_size
    image = image[:height, :width]
    print(f"  Cropped dimensions: {height}x{width}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Slice the image into a 64x64 grid with no overlapping
    patches = patchify(image, (tile_size, tile_size, 3), step=tile_size)
    tile_count = 0

    # Extract and save each individual tile
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            single_patch = patches[i, j, 0]
            save_patch = cv2.cvtColor(single_patch, cv2.COLOR_RGB2BGR)
            # Use region prefix to prevent naming collisions between regions
            tile_name = f"{region_name}_tile_row{i:03d}_col{j:03d}.png"
            cv2.imwrite(os.path.join(output_folder, tile_name), save_patch)
            tile_count += 1

    print(f"  {tile_count} tiles saved to '{output_folder}'")
    return tile_count

if __name__ == "__main__":
    for year in [2020, 2025]:
        output_folder = f'bursa_tiles_{year}'
        total = 0
        for region_name in REGIONS:
            if os.path.exists(f'bursa_raw_data_{year}/{region_name}'):
                total += slice_region(year, region_name, output_folder)
            else:
                print(f"Skipping {region_name} {year} — folder not found")
        print(f"\nTotal tiles for {year}: {total}")