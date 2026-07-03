import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

export default function DimensionCard({ label, score, trend = 'stable', index = 0 }) {
  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus
  const trendColor = trend === 'up' ? 'text-emerald-500' : trend === 'down' ? 'text-red-500' : 'text-slate-400'
  const trendLabel = trend === 'up' ? 'Improving' : trend === 'down' ? 'Declining' : 'Stable'

  const getGradient = () => {
    if (score >= 80) return 'from-emerald-400 to-emerald-600'
    if (score >= 60) return 'from-blue-400 to-blue-600'
    if (score >= 40) return 'from-amber-400 to-amber-600'
    return 'from-red-400 to-red-600'
  }

  const getScoreColor = () => {
    if (score >= 80) return '#10b981'
    if (score >= 60) return '#3b82f6'
    if (score >= 40) return '#f59e0b'
    return '#ef4444'
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.08, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="liquid-glass-sm p-4 flex items-center gap-4 group"
    >
      {/* Score ring */}
      <div className="relative w-14 h-14 flex-shrink-0">
        <svg className="w-14 h-14 -rotate-90" viewBox="0 0 56 56">
          <circle cx="28" cy="28" r="22" fill="none" stroke="rgba(226,232,240,0.4)" strokeWidth="4" />
          <motion.circle
            cx="28" cy="28" r="22" fill="none"
            stroke={getScoreColor()}
            strokeWidth="4.5"
            strokeLinecap="round"
            strokeDasharray={138}
            initial={{ strokeDashoffset: 138 }}
            animate={{ strokeDashoffset: 138 - (138 * score / 100) }}
            transition={{ duration: 1.2, delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm font-black text-slate-700 dark:text-white">{Math.round(score)}</span>
        </div>
      </div>

      {/* Label and bar */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate">{label}</p>
          <div className={`flex items-center gap-1 ${trendColor}`}>
            <TrendIcon className="w-3.5 h-3.5" />
            <span className="text-[10px] font-bold uppercase tracking-wider">{trendLabel}</span>
          </div>
        </div>
        <div className="h-2.5 bg-slate-100/80 dark:bg-slate-700/50 rounded-full overflow-hidden">
          <motion.div
            className={`h-full rounded-full bg-gradient-to-r ${getGradient()} shadow-sm`}
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ duration: 1.2, delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
          />
        </div>
      </div>
    </motion.div>
  )
}
