import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'

export default function HealthScoreRadar({ dimensions }) {
  if (!dimensions) return null

  const data = Object.entries(dimensions).map(([key, value]) => ({
    dimension: value.label,
    score: value.score,
    fullMark: 100,
  }))

  return (
    <div className="w-full h-[300px] md:h-[350px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
          <PolarGrid
            stroke="#e2e8f0"
            strokeDasharray="3 3"
          />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fill: '#64748b', fontSize: 11 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: '#94a3b8', fontSize: 10 }}
          />
          <Radar
            name="Score"
            dataKey="score"
            stroke="#1e3a5f"
            fill="#1e3a5f"
            fillOpacity={0.2}
            strokeWidth={2}
          />
          <Radar
            name="Benchmark"
            dataKey="fullMark"
            stroke="#f59e0b"
            fill="#f59e0b"
            fillOpacity={0.05}
            strokeWidth={1}
            strokeDasharray="5 5"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
              fontSize: '12px',
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
