import DonutChart from "./DonutChart";
import ChangeLineChart from "./ChangeLineChart";

export default function StatsPanel({ selectedDistrict, onBack, data, loading }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

      {/* Back button — only shows when a district is selected */}
      {selectedDistrict && (
        <button onClick={onBack} style={{
          display: "flex", alignItems: "center", gap: 8,
          background: "#3b82f6", color: "white", border: "none",
          borderRadius: 24, padding: "10px 20px", fontSize: 14,
          fontWeight: 600, cursor: "pointer", alignSelf: "flex-end"
        }}>
          ← Bursa Overview
        </button>
      )}

      {loading || !data ? (
        <div style={{
          background: "white", borderRadius: 16, padding: 24,
          textAlign: "center", color: "#9ca3af", fontSize: 14
        }}>
          Loading...
        </div>
      ) : (
        <>
          {selectedDistrict && (
            <p style={{ fontSize: 13, color: "#6b7280", paddingLeft: 4 }}>
              Showing data for <strong style={{ color: "#1a1a1a" }}>{selectedDistrict}</strong>
            </p>
          )}
          <ChangeLineChart changeData={data.change} />
          <DonutChart distribution={data.stats2020?.distribution} year="2020" />
          <DonutChart distribution={data.stats2025?.distribution} year="2025" />
        </>
      )}
    </div>
  );
}