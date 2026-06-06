import os
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig, BBox, bbox_to_dimensions,
    CRS, DataCollection, SentinelHubRequest, MimeType
)

# CDSE API Authentication
load_dotenv()
config = SHConfig()
config.sh_client_id = os.getenv('SH_CLIENT_ID')
config.sh_client_secret = os.getenv('SH_CLIENT_SECRET')
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# 3 regions covering ~10 districts at near 10m resolution each
# West:   Nilüfer, Mudanya, Gemlik, Karacabey edge
# Center: Osmangazi, Yıldırım, Kestel, Gürsu
# East:   İnegöl, Yenişehir, Orhangazi
REGIONS = {
    "west":   [28.65, 40.00, 29.00, 40.40],
    "center": [29.00, 40.00, 29.25, 40.40],
    "east":   [29.25, 40.00, 29.60, 40.40],
}

evalscript_true_color = """
//VERSION=3
function setup() {
    return {
        input: ["B04", "B03", "B02", "dataMask"],
        output: { bands: 3 }
    };
}
function evaluatePixel(sample) {
    return [
        sample.B04 * 2.5 * sample.dataMask,
        sample.B03 * 2.5 * sample.dataMask,
        sample.B02 * 2.5 * sample.dataMask
    ];
}
"""

# Build and send one API request per region per year
def fetch_region(year, region_name, coords):
    print(f"\nRequesting {region_name} region for {year}...")
    bbox = BBox(bbox=coords, crs=CRS.WGS84)
    raw_size = bbox_to_dimensions(bbox, resolution=10)

    # Calculate the largest possible scale factor that keeps both dimensions within 2500x2500 pixels limit
    w, h = raw_size
    if w > 2500 or h > 2500:
        scale_ratio = min(2500 / w, 2500 / h)
        image_size = (int(w * scale_ratio), int(h * scale_ratio))
    else:
        image_size = raw_size

    print(f"  Image size: {image_size[0]} x {image_size[1]} pixels")

    output_folder = f'bursa_raw_data_{year}/{region_name}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C.define_from(
                    "s2l1c_cdse", service_url=config.sh_base_url
                ),
                time_interval=(f'{year}-06-01', f'{year}-08-31'),
                mosaicking_order="leastCC",
                other_args={"dataFilter": {"maxCloudCoverage": 5}}
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default", MimeType.PNG)
        ],
        bbox=bbox,
        size=image_size,
        config=config,
        data_folder=output_folder
    )

    data = request.get_data(save_data=True)
    if data:
        print(f"{region_name} {year} saved to /{output_folder}")
        return data[-1]
    else:
        print(f"No clear image found for {region_name} {year}")
        return None

if __name__ == "__main__":
    all_images = {2020: {}, 2025: {}}  

    for year in [2020, 2025]:
        print(f"\n{'='*40}")
        print(f"Downloading all regions for {year}")
        print(f"{'='*40}")
        for region_name, coords in REGIONS.items():
            img = fetch_region(year, region_name, coords)
            if img is not None:
                all_images[year][region_name] = img 

    print("\nAll downloads complete!")

    # Preview all regions for both years
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Bursa Sentinel-2 Imagery by Region", fontsize=14)

    for row_idx, year in enumerate([2020, 2025]):
        for col_idx, region_name in enumerate(["west", "center", "east"]):
            ax = axes[row_idx][col_idx]
            img = all_images[year].get(region_name)

            if img is not None:
                rgb = img[:, :, :3].astype(np.float32)
                p2 = np.percentile(rgb, 2)
                p98 = np.percentile(rgb, 98)
                rgb = np.clip((rgb - p2) / (p98 - p2 + 1e-6), 0, 1)
                ax.imshow(rgb)
                ax.set_title(f"{year} — {region_name}")
            else:
                ax.text(0.5, 0.5, "No image", ha='center', va='center',
                        transform=ax.transAxes)
                ax.set_title(f"{year} — {region_name} (missing)")

            ax.axis('off')

    plt.tight_layout()
    plt.show()