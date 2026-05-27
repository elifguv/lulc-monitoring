from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="Bursa LULC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any frontend to connect 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_classification_data(year):
    """Helper function to load the JSON file from the hard drive."""
    file_path = f"classification_{year}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Data for {year} not found. Did you run the AI yet?")
    
    with open(file_path, "r") as f:
        return json.load(f)


# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bursa Land Use/Land Cover API! The server is running."}

@app.get("/api/map/2020")
def get_map_2020():
    print("📡 Frontend requested 2020 data...")
    return load_classification_data(2020)

@app.get("/api/map/2025")
def get_map_2025():
    print("📡 Frontend requested 2025 data...")
    return load_classification_data(2025)