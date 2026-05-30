import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { useWindowSize } from "../hooks/useWindowSize";

const CLASS_COLORS = {
  AnnualCrop: "#FFD700", Forest: "#006400",
  HerbaceousVegetation: "#90EE90", Highway: "#808080",
  Industrial: "#800080", Pasture: "#99CC33",
  PermanentCrop: "#FFA500", Residential: "#FF4444",
  River: "#00BFFF", SeaLake: "#1E90FF",
};

export default function DonutChart({ distribution, year }) {
  const { width } = useWindowSize();
  const isTablet = width <= 1024;
  const isMobile = width <= 640;

  if (!distribution) return null;

  const data = Object.entries(distribution)
    .map(([name, val]) => ({ name, value: val.percentage }))
    .filter(d => d.value > 0)
    .sort((a, b) => b.value - a.value);

  // Scale radii down on smaller screens
  const innerRadius = isMobile ? 36 : isTablet ? 44 : 52;
  const outerRadius = isMobile ? 54 : isTablet ? 62 : 76;
  const chartHeight = isMobile ? 140 : 180;
  const yearFontSize = isMobile ? 26 : 36;

  return (
    <div style={{
      background: "white", borderRadius: 16, padding: "16px 20px",
      boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
        <span style={{
          fontSize: yearFontSize, fontWeight: 700, color: "#1a1a1a",
          minWidth: isMobile ? 54 : 72, lineHeight: 1
        }}>
          {year}
        </span>
        <div style={{ flex: 1, height: chartHeight }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%" cy="50%"
                innerRadius={innerRadius}
                outerRadius={outerRadius}
                dataKey="value"
                paddingAngle={2}
                startAngle={90} endAngle={-270}
              >
                {data.map(entry => (
                  <Cell key={entry.name} fill={CLASS_COLORS[entry.name] || "#ccc"} />
                ))}
              </Pie>
              <Tooltip formatter={v => `${v.toFixed(1)}%`} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "4px 14px", marginTop: 10 }}>
        {data.map(entry => (
          <span key={entry.name} style={{
            fontSize: isMobile ? 10 : 11, color: "#444",
            display: "flex", alignItems: "center", gap: 5
          }}>
            <span style={{
              width: 8, height: 8, borderRadius: "50%",
              background: CLASS_COLORS[entry.name] || "#ccc",
              display: "inline-block", flexShrink: 0
            }} />
            {entry.name} <strong>{entry.value.toFixed(1)}%</strong>
          </span>
        ))}
      </div>
    </div>
  );
}