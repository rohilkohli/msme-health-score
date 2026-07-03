import { motion } from 'framer-motion'
import { History as HistoryIcon, Calendar, TrendingUp, TrendingDown, Minus, Filter } from 'lucide-react'
import TrendChart from '../components/TrendChart'
import { useHealthScore } from '../hooks/useHealthScore'
import { getScoreCategory } from '../utils/constants'

const detailedHistory = [
  {
    date: '2026-07-02',
    score: 742,
    change: +7,
    category: 'Good',
    event: 'Monthly recalculation',
    dimensions: { revenue: 78, expense: 65, tax: 92, workforce: 71, banking: 85 },
  },
  {
    date: '2026-06-01',
    score: 735,
    change: +7,
    category: 'Good',
    event: 'GST filing on time bonus',
    dimensions: { revenue: 76, expense: 63, tax: 90, workforce: 72, banking: 83 },
  },
  {
    date: '2026-05-01',
    score: 728,
    change: +23,
    category: 'Good',
    event: 'Revenue growth detected',
    dimensions: { revenue: 74, expense: 62, tax: 88, workforce: 70, banking: 82 },
  },
  {
    date: '2026-04-01',
    score: 705,
    change: -5,
    category: 'Good',
    event: 'Expense spike in Q4',
    dimensions: { revenue: 70, expense: 58, tax: 87, workforce: 71, banking: 80 },
  },
  {
    date: '2026-03-01',
    score: 710,
    change: +15,
    category: 'Good',
    event: 'New client revenue added',
    dimensions: { revenue: 72, expense: 60, tax: 86, workforce: 69, banking: 78 },
  },
  {
    date: '2026-02-01',
    score: 695,
    change: +15,
    category: 'Good',
    event: 'Banking behavior improved',
    dimensions: { revenue: 68, expense: 59, tax: 84, workforce: 68, banking: 77 },
  },
  {
    date: '2026-01-01',
    score: 680,
    change: 0,
    category: 'Fair',
    event: 'Initial assessment',
    dimensions: { revenue: 65, expense: 57, tax: 82, workforce: 67, banking: 75 },
  },
]

export default function History() {
  const { history } = useHealthScore()

  const getChangeIcon = (change) => {
    if (change > 0) return <TrendingUp className="w-4 h-4 text-emerald-500" />
    if (change < 0) return <TrendingDown className="w-4 h-4 text-red-500" />
    return <Minus className="w-4 h-4 text-slate-400" />
  }

  const getChangeText = (change) => {
    if (change > 0) return `+${change}`
    if (change < 0) return `${change}`
    return '0'
  }

  const getChangeColor = (change) => {
    if (change > 0) return 'text-emerald-600'
    if (change < 0) return 'text-red-600'
    return 'text-slate-500'
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <HistoryIcon className="w-6 h-6 text-primary-800" />
            Score History
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Track your financial health score progression over time
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select className="px-3 py-2 rounded-lg border border-slate-300 text-sm text-slate-700 bg-white focus:border-primary-800 outline-none">
            <option>Last 6 months</option>
            <option>Last 12 months</option>
            <option>All time</option>
          </select>
          <button className="flex items-center gap-2 px-3 py-2 rounded-lg border border-slate-300 text-sm text-slate-700 hover:bg-slate-50">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="liquid-glass-sm p-5"
        >
          <p className="text-sm text-slate-500 dark:text-slate-400">Current Score</p>
          <p className="text-3xl font-bold text-primary-800 mt-1">742</p>
          <div className="flex items-center gap-1 mt-2">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-sm text-emerald-600 font-medium">+62 since Jan 2026</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="liquid-glass-sm p-5"
        >
          <p className="text-sm text-slate-500 dark:text-slate-400">Highest Score</p>
          <p className="text-3xl font-bold text-emerald-600 mt-1">742</p>
          <div className="flex items-center gap-1 mt-2">
            <Calendar className="w-4 h-4 text-slate-400" />
            <span className="text-sm text-slate-500">Jul 2026 (Current)</span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="liquid-glass-sm p-5"
        >
          <p className="text-sm text-slate-500 dark:text-slate-400">Avg Monthly Change</p>
          <p className="text-3xl font-bold text-accent-600 mt-1">+8.9</p>
          <div className="flex items-center gap-1 mt-2">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-sm text-emerald-600 font-medium">Consistently improving</span>
          </div>
        </motion.div>
      </div>

      {/* Trend Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="liquid-glass p-6"
      >
        <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">Score Trend</h3>
        <TrendChart data={history} height={300} />
      </motion.div>

      {/* Detailed History Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="liquid-glass p-6"
      >
        <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-6">Assessment Timeline</h3>

        <div className="space-y-4">
          {detailedHistory.map((item, index) => {
            const category = getScoreCategory(item.score)
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.05 }}
                className="flex items-start gap-4 p-4 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
              >
                {/* Timeline dot */}
                <div className="flex flex-col items-center">
                  <div
                    className="w-3 h-3 rounded-full border-2"
                    style={{ borderColor: category.color, backgroundColor: category.bgColor }}
                  ></div>
                  {index < detailedHistory.length - 1 && (
                    <div className="w-0.5 h-full min-h-[40px] bg-slate-200 dark:bg-slate-600 mt-1"></div>
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 -mt-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold text-slate-800 dark:text-white">{item.score}</span>
                      <span
                        className="text-xs font-semibold px-2 py-0.5 rounded-full border"
                        style={{ color: category.color, backgroundColor: category.bgColor, borderColor: category.color + '40' }}
                      >
                        {item.category}
                      </span>
                      <div className="flex items-center gap-1">
                        {getChangeIcon(item.change)}
                        <span className={`text-sm font-medium ${getChangeColor(item.change)}`}>
                          {getChangeText(item.change)}
                        </span>
                      </div>
                    </div>
                    <span className="text-xs text-slate-500">{item.date}</span>
                  </div>
                  <p className="text-sm text-slate-500 mt-1">{item.event}</p>

                  {/* Mini dimension bars */}
                  <div className="flex items-center gap-2 mt-2">
                    {Object.entries(item.dimensions).map(([key, value]) => (
                      <div key={key} className="flex-1">
                        <div className="w-full h-1.5 bg-slate-100 dark:bg-slate-600 rounded-full overflow-hidden">
                          <div
                            className="h-full rounded-full bg-primary-600"
                            style={{ width: `${value}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </motion.div>
  )
}
