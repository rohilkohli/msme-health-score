import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, Activity, TrendingUp, Database, ArrowUpRight, ArrowDownRight, Sparkles, X, Heart, BarChart3, Shield } from 'lucide-react'
import StatsCard from '../components/StatsCard'
import PortfolioChart from '../components/PortfolioChart'
import TrendChart from '../components/TrendChart'
import { useHealthScore } from '../hooks/useHealthScore'

const recentAssessments = [
  { id: 1, business: 'Sharma Textiles Pvt Ltd', gstin: '27AABCS1234A1Z5', score: 812, category: 'Excellent', date: '2026-07-02', industry: 'Textiles', city: 'Mumbai', revenue: 78, cashFlow: 82, compliance: 91, growth: 72, repayment: 85 },
  { id: 2, business: 'Patel Electronics', gstin: '24AABCP5678B2Y3', score: 695, category: 'Good', date: '2026-07-01', industry: 'Manufacturing', city: 'Ahmedabad', revenue: 68, cashFlow: 72, compliance: 75, growth: 60, repayment: 65 },
  { id: 3, business: 'Kumar Auto Parts', gstin: '29AABCK9012C3X1', score: 543, category: 'Fair', date: '2026-06-30', industry: 'Trading', city: 'Bengaluru', revenue: 55, cashFlow: 48, compliance: 62, growth: 50, repayment: 52 },
  { id: 4, business: 'Singh Food Processing', gstin: '07AABCS3456D4W2', score: 728, category: 'Good', date: '2026-06-29', industry: 'Food Processing', city: 'Delhi', revenue: 74, cashFlow: 70, compliance: 80, growth: 68, repayment: 72 },
  { id: 5, business: 'Gupta Pharma Supplies', gstin: '09AABCG7890E5V4', score: 891, category: 'Excellent', date: '2026-06-28', industry: 'Healthcare', city: 'Noida', revenue: 88, cashFlow: 92, compliance: 95, growth: 82, repayment: 90 },
]

const getCategoryStyle = (category) => {
  switch (category) {
    case 'Excellent': return 'bg-emerald-50 text-emerald-700 border-emerald-200 score-excellent'
    case 'Good': return 'bg-blue-50 text-blue-700 border-blue-200 score-good'
    case 'Fair': return 'bg-amber-50 text-amber-700 border-amber-200 score-fair'
    default: return 'bg-red-50 text-red-700 border-red-200 score-poor'
  }
}

export default function Dashboard() {
  const { history } = useHealthScore()
  const [selectedBusiness, setSelectedBusiness] = useState(null)

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Portfolio overview and health assessment analytics
          </p>
        </div>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-accent-50 to-amber-50 border border-accent-200/60"
        >
          <Sparkles className="w-4 h-4 text-accent-500" />
          <span className="text-sm font-medium text-accent-700">AI-Powered Insights Active</span>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
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
          subtitle="1,935 MSMEs qualified"
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
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="liquid-glass p-6"
        >
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-1">
            Portfolio Distribution
          </h3>
          <p className="text-xs text-slate-400 mb-4">Score category breakdown</p>
          <PortfolioChart />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
          className="liquid-glass p-6"
        >
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-1">
            Score Trend
          </h3>
          <p className="text-xs text-slate-400 mb-4">Your business performance over time</p>
          <TrendChart data={history} height={250} />
        </motion.div>
      </div>

      {/* Recent Assessments */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="liquid-glass overflow-hidden"
      >
        <div className="p-6 border-b border-slate-100 dark:border-slate-700/50">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Recent Assessments</h3>
              <p className="text-xs text-slate-400 mt-0.5">Latest financial health evaluations</p>
            </div>
            <button className="text-sm font-medium text-primary-800 hover:text-primary-600 transition-colors">
              View All
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-slate-50/80 dark:bg-slate-900/50">
                <th className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-6 py-3">Business</th>
                <th className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-6 py-3">GSTIN</th>
                <th className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-6 py-3">Score</th>
                <th className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-6 py-3">Category</th>
                <th className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-6 py-3">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50 dark:divide-slate-800">
              {recentAssessments.map((item, idx) => (
                <motion.tr
                  key={item.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.6 + idx * 0.05 }}
                  onClick={() => setSelectedBusiness(item)}
                  className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors cursor-pointer"
                >
                  <td className="px-6 py-4">
                    <p className="text-sm font-semibold text-slate-800 dark:text-white">{item.business}</p>
                  </td>
                  <td className="px-6 py-4">
                    <p className="text-sm text-slate-500 font-mono text-xs">{item.gstin}</p>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1.5">
                      <span className="text-sm font-bold text-slate-800 dark:text-white">{item.score}</span>
                      {item.score > 700 ? (
                        <ArrowUpRight className="w-3.5 h-3.5 text-emerald-500" />
                      ) : (
                        <ArrowDownRight className="w-3.5 h-3.5 text-amber-500" />
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex text-[11px] font-bold px-2.5 py-1 rounded-lg border ${getCategoryStyle(item.category)}`}>
                      {item.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <p className="text-sm text-slate-400">{item.date}</p>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Business Detail Modal */}
      <AnimatePresence>
        {selectedBusiness && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setSelectedBusiness(null)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="liquid-glass w-full max-w-lg p-0 overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="gradient-primary p-6 relative">
                <button
                  onClick={() => setSelectedBusiness(null)}
                  className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
                >
                  <X className="w-4 h-4 text-white" />
                </button>
                <h3 className="text-xl font-bold text-white">{selectedBusiness.business}</h3>
                <p className="text-primary-200 text-sm mt-1">{selectedBusiness.industry} • {selectedBusiness.city}</p>
                <p className="text-primary-300 text-xs mt-1 font-mono">GSTIN: {selectedBusiness.gstin}</p>
              </div>

              {/* Score */}
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <p className="text-sm text-slate-500">Composite Score</p>
                    <p className="text-4xl font-black text-slate-800">{selectedBusiness.score}</p>
                  </div>
                  <span className={`px-4 py-2 rounded-xl text-sm font-bold border ${getCategoryStyle(selectedBusiness.category)}`}>
                    {selectedBusiness.category}
                  </span>
                </div>

                {/* Dimension Bars */}
                <div className="space-y-3">
                  {[
                    { label: 'Revenue Stability', value: selectedBusiness.revenue, icon: BarChart3, color: 'from-blue-400 to-blue-600' },
                    { label: 'Cash Flow Health', value: selectedBusiness.cashFlow, icon: Activity, color: 'from-emerald-400 to-emerald-600' },
                    { label: 'Compliance Score', value: selectedBusiness.compliance, icon: Shield, color: 'from-violet-400 to-violet-600' },
                    { label: 'Growth Trajectory', value: selectedBusiness.growth, icon: TrendingUp, color: 'from-amber-400 to-amber-600' },
                    { label: 'Repayment Capacity', value: selectedBusiness.repayment, icon: Heart, color: 'from-rose-400 to-rose-600' },
                  ].map((dim, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <dim.icon className="w-4 h-4 text-slate-400 flex-shrink-0" />
                      <div className="flex-1">
                        <div className="flex justify-between mb-1">
                          <span className="text-xs font-medium text-slate-600">{dim.label}</span>
                          <span className="text-xs font-bold text-slate-800">{dim.value}</span>
                        </div>
                        <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                          <motion.div
                            className={`h-full rounded-full bg-gradient-to-r ${dim.color}`}
                            initial={{ width: 0 }}
                            animate={{ width: `${dim.value}%` }}
                            transition={{ duration: 0.8, delay: i * 0.1, ease: 'easeOut' }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <p className="text-xs text-slate-400 mt-4 text-center">
                  Assessed on {selectedBusiness.date}
                </p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
