import { AlertCircle, ArrowRight, CheckCircle2, Clock } from 'lucide-react'
import { motion } from 'framer-motion'

export default function RecommendationList({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null

  // Normalize: backend sends strings, mock sends {text, priority} objects
  const normalized = recommendations.map((rec, i) => {
    if (typeof rec === 'string') {
      const priority = i === 0 ? 'high' : i < 3 ? 'medium' : 'low'
      return { text: rec, priority }
    }
    return rec
  })

  const getPriorityConfig = (priority) => {
    switch (priority) {
      case 'high':
        return {
          icon: AlertCircle,
          color: 'text-red-600',
          bg: 'bg-red-50/80',
          border: 'border-red-200/60',
          badge: 'bg-red-100 text-red-700',
          label: 'High Priority',
        }
      case 'medium':
        return {
          icon: Clock,
          color: 'text-amber-600',
          bg: 'bg-amber-50/80',
          border: 'border-amber-200/60',
          badge: 'bg-amber-100 text-amber-700',
          label: 'Medium Priority',
        }
      default:
        return {
          icon: CheckCircle2,
          color: 'text-blue-600',
          bg: 'bg-blue-50/80',
          border: 'border-blue-200/60',
          badge: 'bg-blue-100 text-blue-700',
          label: 'Low Priority',
        }
    }
  }

  return (
    <div className="space-y-3">
      {normalized.map((rec, index) => {
        const config = getPriorityConfig(rec.priority)
        const Icon = config.icon
        return (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`flex items-start gap-3 p-4 rounded-xl border ${config.border} ${config.bg} backdrop-blur-sm`}
          >
            <Icon className={`w-5 h-5 ${config.color} mt-0.5 flex-shrink-0`} />
            <div className="flex-1">
              <p className="text-sm font-medium text-slate-700">{rec.text}</p>
              <span className={`inline-block mt-2 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${config.badge}`}>
                {config.label}
              </span>
            </div>
            <ArrowRight className="w-4 h-4 text-slate-400 mt-0.5" />
          </motion.div>
        )
      })}
    </div>
  )
}
