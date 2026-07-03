import { motion } from 'framer-motion'
import {
  Heart,
  TrendingUp,
  TrendingDown,
  Minus,
  Shield,
  AlertTriangle,
  Clock,
  CheckCircle2,
  Download,
  Share2,
  RefreshCw,
} from 'lucide-react'
import ScoreGauge from '../components/ScoreGauge'
import HealthScoreRadar from '../components/HealthScoreRadar'
import DimensionCard from '../components/DimensionCard'
import RecommendationList from '../components/RecommendationList'
import RiskIndicator from '../components/RiskIndicator'
import { useHealthScore } from '../hooks/useHealthScore'
import { formatDateTime } from '../utils/formatters'
import { getScoreCategory } from '../utils/constants'

export default function HealthCard() {
  const { healthScore, loading } = useHealthScore()

  if (loading || !healthScore) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-800 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600 font-medium">Computing your health score...</p>
        </div>
      </div>
    )
  }

  const category = getScoreCategory(healthScore.composite_score)
  const riskLevel = healthScore.composite_score >= 700 ? 'low' : healthScore.composite_score >= 500 ? 'medium' : 'high'

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
            <Heart className="w-6 h-6 text-red-500" />
            Financial Health Card
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Comprehensive multidimensional assessment of your business
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-300 text-slate-700 text-sm font-medium hover:bg-slate-50 transition-colors">
            <Download className="w-4 h-4" />
            Export PDF
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-300 text-slate-700 text-sm font-medium hover:bg-slate-50 transition-colors">
            <Share2 className="w-4 h-4" />
            Share
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-800 text-white text-sm font-medium hover:bg-primary-700 transition-colors">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {/* Main Score Card */}
      <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden">
        <div className="gradient-primary p-8 text-center relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PHBhdGggZD0iTTM2IDM0djZoNnYtNmgtNnptMC0zMHY2aDZ2LTZoLTZ6Ii8+PC9nPjwvZz48L3N2Zz4=')] opacity-50"></div>
          <div className="relative">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <ScoreGauge score={healthScore.composite_score} size={220} />
            </motion.div>
            <div className="mt-4 flex items-center justify-center gap-4">
              <RiskIndicator level={riskLevel} size="md" />
              <div className="flex items-center gap-1 text-white/80 text-sm">
                <Clock className="w-4 h-4" />
                Updated: {formatDateTime(healthScore.last_updated)}
              </div>
            </div>
          </div>
        </div>

        {/* Radar + Dimensions */}
        <div className="p-6 md:p-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Radar Chart */}
            <div>
              <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
                Dimension Overview
              </h3>
              <HealthScoreRadar dimensions={healthScore.dimensions} />
            </div>

            {/* Dimension Cards */}
            <div>
              <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
                Individual Scores
              </h3>
              <div className="space-y-3">
                {Object.entries(healthScore.dimensions).map(([key, dim], index) => (
                  <DimensionCard
                    key={key}
                    label={dim.label}
                    score={dim.score}
                    trend={dim.trend}
                    index={index}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strengths */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-emerald-200 dark:border-slate-700"
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Strengths</h3>
          </div>
          <ul className="space-y-3">
            {healthScore.strengths.map((strength, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className="flex items-start gap-2"
              >
                <TrendingUp className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-slate-600 dark:text-slate-300">{strength}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>

        {/* Weaknesses */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-red-200 dark:border-slate-700"
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Areas of Concern</h3>
          </div>
          <ul className="space-y-3">
            {healthScore.weaknesses.map((weakness, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className="flex items-start gap-2"
              >
                <TrendingDown className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-slate-600 dark:text-slate-300">{weakness}</span>
              </motion.li>
            ))}
          </ul>
        </motion.div>
      </div>

      {/* Recommendations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700"
      >
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 bg-accent-100 rounded-lg flex items-center justify-center">
            <Shield className="w-5 h-5 text-accent-600" />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
            Actionable Recommendations
          </h3>
        </div>
        <RecommendationList recommendations={healthScore.recommendations} />
      </motion.div>
    </motion.div>
  )
}
