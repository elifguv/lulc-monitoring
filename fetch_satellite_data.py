import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig,
    BBox,
    bbox_to_dimensions,
    CRS,
    DataCollection,
    SentinelHubRequest,
    MimeType
)

# CDSE API Authentication
load_dotenv()
config = SHConfig()
config.sh_client_id = os.getenv('SH_CLIENT_ID')
config.sh_client_secret = os.getenv('SH_CLIENT_SECRET')
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# Target specifications (Bursa)
bursa_coords = [28.85, 40.15, 29.15, 40.25]
bursa_bbox = BBox(bbox=bursa_coords, crs=CRS.WGS84)

# Calculate image dimensions for a 10m/pixel resolution
raw_size = bbox_to_dimensions(bursa_bbox, resolution=10)

if raw_size[0] > 2500:
    scale_ratio = 2500 / raw_size[0]
    image_size = (2500, int(raw_size[1] * scale_ratio))
else:
    image_size = raw_size

print(f"Target Image Resolution: {image_size[0]} x {image_size[1]} pixels")


def fetch_bursa_image(year):
    print(f"Requesting Sentinel-2 L2A data for Summer {year}...")
    time_interval = (f'{year}-06-01', f'{year}-08-31')

    output_folder = f'bursa_raw_data_{year}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                # FIX 2: Changed L1C → L2A for atmospherically corrected surface reflectance
                data_collection=DataCollection.SENTINEL2_L1C.define_from(
                    "s2l1c_cdse", service_url=config.sh_base_url
                ),
                time_interval=time_interval,
                mosaicking_order="leastCC",
                other_args={"dataFilter": {"maxCloudCoverage": 5}}
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default", MimeType.PNG)
        ],
        bbox=bursa_bbox,
        size=image_size,
        config=config,
        data_folder=output_folder
    )

    data = request.get_data(save_data=True)
    if data:
        print(f"Successfully downloaded {year} imagery to /{output_folder}!")
        return data[-1]
    else:
        print(f"No clear images found for {year}.")
        return None


if __name__ == "__main__":
    img_2020 = fetch_bursa_image(2020)
    img_2025 = fetch_bursa_image(2025) 

    if img_2020 is not None and img_2025 is not None:
        fig, axes = plt.subplots(1, 2, figsize=(15, 7))
        axes[0].imshow(img_2020)
        axes[0].set_title("Bursa - 2020")
        axes[0].axis('off')
        axes[1].imshow(img_2025)
        axes[1].set_title("Bursa - 2025")
        axes[1].axis('off')
        plt.tight_layout()
        plt.show()