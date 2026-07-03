import { useState } from 'react'
import { motion } from 'framer-motion'
import LoanApplicationModal from '../components/LoanApplicationModal'
import {
  CreditCard,
  TrendingUp,
  Building,
  Target,
  ArrowRight,
  CheckCircle2,
  Star,
  Percent,
  IndianRupee,
  BarChart3,
} from 'lucide-react'
import { useHealthScore } from '../hooks/useHealthScore'

export default function CreditAssessment() {
  const { creditAssessment, loading } = useHealthScore()
  const [applyingProduct, setApplyingProduct] = useState(null)

  if (loading || !creditAssessment) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-800 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600 font-medium">Analyzing credit readiness...</p>
        </div>
      </div>
    )
  }

  const readiness = creditAssessment.credit_readiness

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
          <CreditCard className="w-6 h-6 text-primary-800" />
          Credit Assessment
        </h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
          Your credit readiness and eligible loan products
        </p>
      </div>

      {/* Credit Readiness Meter */}
      <div className="liquid-glass p-8">
        <div className="text-center mb-8">
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-2">
            Credit Readiness Score
          </h3>
          <p className="text-sm text-slate-500">Based on your current financial health profile</p>
        </div>

        <div className="max-w-lg mx-auto">
          {/* Readiness bar */}
          <div className="relative mb-4">
            <div className="w-full h-6 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full relative"
                style={{
                  background: `linear-gradient(90deg, #ef4444 0%, #f59e0b 40%, #10b981 80%, #059669 100%)`,
                }}
                initial={{ width: 0 }}
                animate={{ width: `${readiness}%` }}
                transition={{ duration: 1.5, ease: 'easeOut' }}
              />
            </div>
            <motion.div
              className="absolute top-8 flex flex-col items-center"
              initial={{ opacity: 0, left: '0%' }}
              animate={{ opacity: 1, left: `${readiness}%` }}
              transition={{ duration: 1.5, ease: 'easeOut' }}
              style={{ transform: 'translateX(-50%)' }}
            >
              <div className="w-0 h-0 border-l-[6px] border-r-[6px] border-b-[8px] border-transparent border-b-primary-800"></div>
              <span className="text-sm font-bold text-primary-800 mt-1">{readiness}%</span>
            </motion.div>
          </div>

          <div className="flex justify-between text-xs text-slate-400 mt-10">
            <span>Not Ready</span>
            <span>Partially Ready</span>
            <span>Mostly Ready</span>
            <span>Fully Ready</span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
          <div className="text-center p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
            <p className="text-2xl font-bold text-primary-800">{creditAssessment.industry_benchmark.your_percentile}th</p>
            <p className="text-xs text-slate-500 mt-1">Percentile in Industry</p>
          </div>
          <div className="text-center p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
            <p className="text-2xl font-bold text-emerald-600">{creditAssessment.eligible_products.length}</p>
            <p className="text-xs text-slate-500 mt-1">Eligible Products</p>
          </div>
          <div className="text-center p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
            <p className="text-2xl font-bold text-accent-600">1.2 Cr</p>
            <p className="text-xs text-slate-500 mt-1">Max Eligible Amount</p>
          </div>
        </div>
      </div>

      {/* Industry Benchmark Comparison */}
      <div className="liquid-glass p-6">
        <div className="flex items-center gap-2 mb-6">
          <BarChart3 className="w-5 h-5 text-primary-800" />
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Industry Benchmark</h3>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-600 dark:text-slate-300">Your Score</span>
            <span className="text-sm font-bold text-primary-800">742</span>
          </div>
          <div className="relative w-full h-3 bg-slate-100 dark:bg-slate-700 rounded-full">
            <div className="absolute h-full bg-primary-800 rounded-full" style={{ width: '74.2%' }}></div>
            <div
              className="absolute top-0 w-0.5 h-full bg-amber-500"
              style={{ left: '65%' }}
              title="Industry Average"
            ></div>
            <div
              className="absolute top-0 w-0.5 h-full bg-emerald-500"
              style={{ left: '78%' }}
              title="Top Quartile"
            ></div>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span>0</span>
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                Avg: {creditAssessment.industry_benchmark.average_score}
              </span>
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                Top 25%: {creditAssessment.industry_benchmark.top_quartile}
              </span>
            </div>
            <span>1000</span>
          </div>
        </div>
      </div>

      {/* Eligible Products */}
      <div className="liquid-glass p-6">
        <div className="flex items-center gap-2 mb-6">
          <Star className="w-5 h-5 text-accent-500" />
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Eligible Loan Products</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {creditAssessment.eligible_products.map((product, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="border border-slate-200 dark:border-slate-600 rounded-xl p-5 hover:border-primary-300 hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <h4 className="font-semibold text-slate-800 dark:text-white text-sm">{product.name}</h4>
                <span className="text-xs bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full font-medium border border-emerald-200">
                  Pre-approved
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500 flex items-center gap-1">
                    <IndianRupee className="w-3 h-3" /> Limit
                  </span>
                  <span className="text-sm font-bold text-slate-800 dark:text-white">
                    {product.limit}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500 flex items-center gap-1">
                    <Percent className="w-3 h-3" /> Interest
                  </span>
                  <span className="text-sm font-semibold text-emerald-600">{product.interest} p.a.</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500 flex items-center gap-1">
                    <Building className="w-3 h-3" /> Provider
                  </span>
                  <span className="text-sm text-slate-700 dark:text-slate-300">{product.provider}</span>
                </div>
              </div>

              <button
                onClick={() => setApplyingProduct(product)}
                className="w-full mt-4 flex items-center justify-center gap-2 bg-primary-50 text-primary-800 py-2 rounded-lg text-sm font-medium hover:bg-primary-100 transition-colors"
              >
                Apply Now
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Improvement Areas */}
      <div className="liquid-glass p-6">
        <div className="flex items-center gap-2 mb-6">
          <Target className="w-5 h-5 text-primary-800" />
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">How to Improve Your Score</h3>
        </div>

        <div className="space-y-3">
          {creditAssessment.improvement_areas.map((area, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-700 rounded-lg"
            >
              <div className="flex-shrink-0 w-8 h-8 bg-primary-800 text-white rounded-full flex items-center justify-center text-sm font-bold">
                {index + 1}
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-slate-800 dark:text-white">{area.area}</p>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-emerald-600 font-semibold flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    {area.impact}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    area.effort === 'Low' ? 'bg-emerald-50 text-emerald-700' :
                    area.effort === 'Medium' ? 'bg-amber-50 text-amber-700' :
                    'bg-red-50 text-red-700'
                  }`}>
                    {area.effort} Effort
                  </span>
                </div>
              </div>
              <CheckCircle2 className="w-5 h-5 text-slate-300" />
            </motion.div>
          ))}
        </div>
      </div>
      {/* Loan Application Modal */}
      {applyingProduct && (
        <LoanApplicationModal
          product={applyingProduct}
          onClose={() => setApplyingProduct(null)}
        />
      )}
    </motion.div>
  )
}
