import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function BursaMap({ selectedDistrict, onDistrictClick }) {
  const [geojson, setGeojson] = useState(null);

  useEffect(() => {
    fetch("/bursa_districts.geojson")
      .then(r => r.json())
      .then(data => {
        // Filter out any broken data 
        const cleaned = {
          ...data,
          features: data.features.filter(f => f.properties && f.properties.name != null)
        };
        setGeojson(cleaned);
      })
      .catch(e => console.error("Failed to load GeoJSON:", e));
  }, []);

  if (!geojson) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
        Loading interactive map...
      </div>
    );
  }

  // Define the colors and borders for the districts
  const styleFeature = (feature) => {
    const isSelected = feature.properties.name === selectedDistrict;
    return {
      fillColor: isSelected ? "#3b82f6" : "#9ca3af",
      weight: isSelected ? 2 : 1.5,
      color: "white",
      fillOpacity: isSelected ? 0.75 : 0.45 // Slightly transparent to see the roads underneath
    };
  };

  // Attach hover effects and click events to every district
  const onEachFeature = (feature, layer) => {
    const districtName = feature.properties.name;
    
    // Add the tooltip
    layer.bindTooltip(`<b>${districtName}</b>`, { sticky: true, direction: "center" });

    layer.on({
      mouseover: (e) => {
        if (districtName !== selectedDistrict) {
          e.target.setStyle({ fillOpacity: 0.7, fillColor: "#6b7280" });
        }
      },
      mouseout: (e) => {
        // Reset to default style when mouse leaves
        e.target.setStyle(styleFeature(feature));
      },
      click: () => {
        onDistrictClick(districtName);
      }
    });
  };

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: "16px", overflow: "hidden" }}>
      <MapContainer
        center={[40.1828, 29.0667]} // GPS coordinates for the center of Bursa
        zoom={9}
        style={{ width: "100%", height: "100%" }}
      >
        {/* The base map underneath data */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
        />
        
        {/* District Polygons */}
        <GeoJSON
          key={selectedDistrict || "none"} // Redraw styles when selection changes
          data={geojson}
          style={styleFeature}
          onEachFeature={onEachFeature}
        />
      </MapContainer>
    </div>
  );
}