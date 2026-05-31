import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from "recharts";
import { useWindowSize } from "../hooks/useWindowSize";

export default function ChangeLineChart({ changeData }) {
  const { width } = useWindowSize();
  const isMobile = width <= 640;

  if (!changeData) return null;

  const data = Object.entries(changeData.change_by_class).map(([cls, val]) => ({
    name: cls.replace(/([A-Z])/g, ' $1').trim(),
    "2020": val["2020"],
    "2025": val["2025"],
  }));

  return (
    <div style={{
      background: "white", borderRadius: 16, padding: "16px 20px",
      boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
    }}>
      <p style={{ fontSize: 12, color: "#6b7280", marginBottom: 12 }}>
        Land cover change 2020 → 2025
      </p>
      <ResponsiveContainer width="100%" height={isMobile ? 120 : 160}>
        <LineChart
          data={data}
          margin={{
            top: 4,
            right: 8,
            left: isMobile ? -28 : -20,
            bottom: isMobile ? 48 : 56
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: isMobile ? 8 : 9 }}
            interval={0}
            angle={-35}
            textAnchor="end"
          />
          <YAxis tick={{ fontSize: 10 }} tickFormatter={v => `${v}%`} />
          <Tooltip formatter={v => `${v.toFixed(1)}%`} />
          <Legend 
            verticalAlign="top"        // ← moves legend above the chart
            align="right"
            wrapperStyle={{ fontSize: 11 }} />
          <Line type="monotone" dataKey="2020" stroke="#93c5fd" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="2025" stroke="#1d4ed8" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer> 
    </div>
  );
}