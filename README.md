# Bursa Land Cover Change Analysis

Analysis of land use and land cover (LULC) change in Bursa province for the 2020–2025 period using Sentinel-2 satellite imagery and deep learning, visualized through an interactive web platform.

This project was developed as a graduation thesis in the Department of Computer Engineering at Bursa Technical University.

## Overview

The system trains an ImageNet-pretrained ResNet-50 model on the EuroSAT dataset via transfer learning, then applies this model to Sentinel-2 imagery of Bursa to reveal district-level land cover distribution and year-over-year change. Results are presented through a React-based interactive web dashboard.

## System Architecture

The system is an end-to-end pipeline composed of six components:

```
Data Retrieval → Image Slicing → Model Inference → Spatial Join → REST API → Web Dashboard
```

1. **Data Retrieval** — Downloading Sentinel-2 L1C satellite imagery from the Copernicus Data Space Ecosystem (CDSE) via the sentinelhub library
2. **Image Slicing** — Splitting images into 64×64 pixel tiles
3. **Model Inference** — Assigning each tile to one of ten land cover classes using ResNet-50
4. **Spatial Join** — Matching tiles to OpenStreetMap district boundaries
5. **REST API** — Serving statistical results via FastAPI
6. **Web Dashboard** — Interactive visualization with React, Leaflet, and Recharts

## Model

- **Architecture:** ResNet-50 (ImageNet-pretrained)
- **Dataset:** EuroSAT RGB (10 classes, 27,000 images)
- **Training strategy:** Two-stage transfer learning
  - Stage 1: Backbone frozen, classification head trained with Adam
  - Stage 2: All layers unfrozen, fine-tuning with low-learning-rate SGD
- **Accuracy:** 98% on the EuroSAT validation set

### Land Cover Classes

AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop, Residential, River, SeaLake

## Study Area

The study area is divided into three geographic regions to preserve resolution within the API size limit:

| Region | Coordinate Bounds | Districts |
|--------|-------------------|-----------|
| West | 28.65°–29.00°E, 40.00°–40.40°N | Nilüfer, Mudanya, Gemlik |
| Central | 29.00°–29.25°E, 40.00°–40.40°N | Osmangazi, Yıldırım, Kestel, Gürsu |
| East | 29.25°–29.60°E, 40.00°–40.40°N | İnegöl, Yenişehir, Orhangazi |

## Tech Stack

**Machine Learning & Data Processing**
- TensorFlow / Keras (ResNet-50)
- sentinelhub (Sentinel-2 data access)
- Shapely (spatial analysis)
- NumPy

**Backend**
- FastAPI
- Uvicorn

**Frontend**
- React
- Leaflet (map)
- Recharts (charts)

## Installation

### Requirements

- Python 3.10+
- Node.js 16+
- A CDSE account (for Sentinel-2 data)

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn server:app --reload
```

The server runs at `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Frontend

```bash
cd bursa-dashboard
npm install
npm run dev
```

## Usage

Run the pipeline in order:

```bash
# 1. Download satellite imagery
python fetch_satellite_data.py

# 2. Slice images into tiles
python slice_images.py

# 3. Classify tiles
python classify_tiles.py

# 4. Spatial join
python spatial_join.py

# 5. Start the backend
uvicorn server:app --reload
```

Then start the web dashboard and explore districts on the map.

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/stats/{year}` | Province-wide class distribution |
| `/api/district/{name}/stats/{year}` | District-level class distribution |
| `/api/district/{name}/change` | 2020–2025 change analysis |

## Findings

- A notable expansion of the PermanentCrop class was detected in the İnegöl and Yenişehir districts, and this finding was validated against TÜİK (Turkish Statistical Institute) crop production statistics.
- The model distinguished major geographic features (the Sea of Marmara, the forests of Mount Uludağ, urban centers) in a geographically consistent manner.

## Known Limitations

- **Domain gap:** Because EuroSAT is Europe-based, the HerbaceousVegetation class is disproportionately dominant and the Industrial class is underrepresented.
- **Small districts:** Statistical reliability is limited in districts with a low tile count.
- **Absolute vs. change:** While the system is affected by the domain gap in absolute classification, it produces reliable results for year-over-year change detection.

