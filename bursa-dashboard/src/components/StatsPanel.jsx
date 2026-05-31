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

          {selectedDistrict && data.stats2020 && data.stats2020.total_tiles < 20 && (
            <div style={{
              background: "#fef9c3", border: "1px solid #fde047",
              borderRadius: 10, padding: "10px 14px",
              fontSize: 12, color: "#854d0e", lineHeight: 1.5
            }}>
              ⚠️ <strong>{selectedDistrict}</strong> only has{" "}
              <strong>{data.stats2020.total_tiles} tiles</strong> — statistics
              may not be reliable for this district.
            </div>
          )}
          
          <ChangeLineChart changeData={data.change} />
          <DonutChart distribution={data.stats2020?.distribution} year="2020" />
          <DonutChart distribution={data.stats2025?.distribution} year="2025" />
        </>
      )}
    </div>
  );
}