import { motion } from 'framer-motion'
import { Users, Activity, TrendingUp, Database, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import StatsCard from '../components/StatsCard'
import PortfolioChart from '../components/PortfolioChart'
import TrendChart from '../components/TrendChart'
import { useHealthScore } from '../hooks/useHealthScore'

const recentAssessments = [
  { id: 1, business: 'Sharma Textiles Pvt Ltd', gstin: '27AABCS1234A1Z5', score: 812, category: 'Excellent', date: '2026-07-02' },
  { id: 2, business: 'Patel Electronics', gstin: '24AABCP5678B2Y3', score: 695, category: 'Good', date: '2026-07-01' },
  { id: 3, business: 'Kumar Auto Parts', gstin: '29AABCK9012C3X1', score: 543, category: 'Fair', date: '2026-06-30' },
  { id: 4, business: 'Singh Food Processing', gstin: '07AABCS3456D4W2', score: 728, category: 'Good', date: '2026-06-29' },
  { id: 5, business: 'Gupta Pharma Supplies', gstin: '09AABCG7890E5V4', score: 891, category: 'Excellent', date: '2026-06-28' },
]

const getCategoryStyle = (category) => {
  switch (category) {
    case 'Excellent': return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case 'Good': return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Fair': return 'bg-amber-50 text-amber-700 border-amber-200'
    case 'Poor': return 'bg-orange-50 text-orange-700 border-orange-200'
    default: return 'bg-red-50 text-red-700 border-red-200'
  }
}

export default function Dashboard() {
  const { history } = useHealthScore()

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Dashboard</h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
          Overview of MSME financial health assessments
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total MSMEs Assessed"
          value="2,847"
          subtitle="+124 this month"
          icon={Users}
          color="primary"
          index={0}
        />
        <StatsCard
          title="Average Health Score"
          value="687"
          subtitle="Up 12 points"
          icon={Activity}
          color="accent"
          index={1}
        />
        <StatsCard
          title="Credit Ready"
          value="68%"
          subtitle="1,935 MSMEs"
          icon={TrendingUp}
          color="success"
          index={2}
        />
        <StatsCard
          title="Active Data Sources"
          value="11,234"
          subtitle="Across all users"
          icon={Database}
          color="info"
          index={3}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700"
        >
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
            Portfolio Distribution
          </h3>
          <PortfolioChart />
        </motion.div>

        {/* Score Trend */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700"
        >
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
            Score Trend (Your Business)
          </h3>
          <TrendChart data={history} height={250} />
        </motion.div>
      </div>

      {/* Recent Assessments */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden"
      >
        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
            Recent Assessments
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 dark:bg-slate-900">
              <tr>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Business</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">GSTIN</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Score</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Category</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
              {recentAssessments.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
                  <td className="px-6 py-4">
                    <p className="text-sm font-medium text-slate-800 dark:text-white">{item.business}</p>
                  </td>
                  <td className="px-6 py-4">
                    <p className="text-sm text-slate-500 font-mono">{item.gstin}</p>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1">
                      <span className="text-sm font-bold text-slate-800 dark:text-white">{item.score}</span>
                      {item.score > 700 ? (
                        <ArrowUpRight className="w-3.5 h-3.5 text-emerald-500" />
                      ) : (
                        <ArrowDownRight className="w-3.5 h-3.5 text-red-500" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex text-xs font-semibold px-2.5 py-0.5 rounded-full border ${getCategoryStyle(item.category)}`}>
                      {item.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <p className="text-sm text-slate-500">{item.date}</p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </motion.div>
  )
}
