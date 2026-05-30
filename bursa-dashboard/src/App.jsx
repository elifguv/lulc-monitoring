import { useState, useEffect } from "react";
import BursaMap from "./components/BursaMap";
import StatsPanel from "./components/StatsPanel";
import "./App.css";

const API = "http://localhost:8000";

export default function App() {
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [overviewData, setOverviewData] = useState(null);
  const [districtData, setDistrictData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load province-wide overview on mount
  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/stats/2020`).then(r => r.json()),
      fetch(`${API}/api/stats/2025`).then(r => r.json()),
      fetch(`${API}/api/change`).then(r => r.json()),
    ]).then(([stats2020, stats2025, change]) => {
      setOverviewData({ stats2020, stats2025, change });
      setLoading(false);
    });
  }, []);

  // Load district-specific data when a district is clicked
  useEffect(() => {
    if (!selectedDistrict) { setDistrictData(null); return; }
    setLoading(true);

    const query = `?district=${encodeURIComponent(selectedDistrict)}`;
    
    Promise.all([
      fetch(`${API}/api/stats/2020${query}`).then(r => r.json()),
      fetch(`${API}/api/stats/2025${query}`).then(r => r.json()),
      fetch(`${API}/api/change${query}`).then(r => r.json()),
    ]).then(([stats2020, stats2025, change]) => {
      setDistrictData({ stats2020, stats2025, change });
      setLoading(false);
    }).catch(err => {
      console.error("Failed to fetch district data:", err);
      setLoading(false);
    });
  }, [selectedDistrict]);

  return (
    <div className="app">
      <div className="map-section">
        <BursaMap
          selectedDistrict={selectedDistrict}
          onDistrictClick={setSelectedDistrict}
        />
      </div>
      <div className="panel-section">
        <StatsPanel
          selectedDistrict={selectedDistrict}
          onBack={() => setSelectedDistrict(null)}
          data={selectedDistrict ? districtData : overviewData}
          loading={loading}
        />
      </div>
    </div>
  );
}