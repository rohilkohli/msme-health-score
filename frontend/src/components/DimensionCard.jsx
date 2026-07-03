import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { motion } from 'framer-motion'

export default function DimensionCard({ label, score, trend, index = 0 }) {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-emerald-500" />
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />
      default:
        return <Minus className="w-4 h-4 text-slate-400" />
    }
  }

  const getTrendLabel = () => {
    switch (trend) {
      case 'up': return 'Improving'
      case 'down': return 'Declining'
      default: return 'Stable'
    }
  }

  const getScoreColor = () => {
    if (score >= 80) return 'bg-emerald-500'
    if (score >= 60) return 'bg-blue-500'
    if (score >= 40) return 'bg-amber-500'
    return 'bg-red-500'
  }

  const getScoreBarBg = () => {
    if (score >= 80) return 'bg-emerald-100'
    if (score >= 60) return 'bg-blue-100'
    if (score >= 40) return 'bg-amber-100'
    return 'bg-red-100'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700 hover:shadow-md transition-shadow"
    >
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-200">{label}</h4>
        <div className="flex items-center gap-1">
          {getTrendIcon()}
          <span className="text-xs text-slate-500">{getTrendLabel()}</span>
        </div>
      </div>
      <div className="flex items-end justify-between mb-2">
        <span className="text-2xl font-bold text-slate-800 dark:text-white">{score}</span>
        <span className="text-xs text-slate-400">/ 100</span>
      </div>
      <div className={`w-full h-2 rounded-full ${getScoreBarBg()}`}>
        <motion.div
          className={`h-full rounded-full ${getScoreColor()}`}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ delay: index * 0.1 + 0.3, duration: 0.8, ease: 'easeOut' }}
        />
      </div>
    </motion.div>
  )
}
