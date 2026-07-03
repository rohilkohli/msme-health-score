import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

const defaultData = [
  { name: 'Excellent (800+)', value: 15, color: '#10b981' },
  { name: 'Good (650-799)', value: 35, color: '#3b82f6' },
  { name: 'Fair (500-649)', value: 28, color: '#f59e0b' },
  { name: 'Poor (350-499)', value: 15, color: '#f97316' },
  { name: 'Critical (<350)', value: 7, color: '#ef4444' },
]

export default function PortfolioChart({ data = defaultData }) {
  return (
    <div className="w-full h-[280px]">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={90}
            paddingAngle={3}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
              fontSize: '12px',
            }}
            formatter={(value) => [`${value}%`, 'Percentage']}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value) => (
              <span className="text-xs text-slate-600">{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
