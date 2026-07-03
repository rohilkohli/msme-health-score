import { motion } from 'framer-motion'

export default function StatsCard({ title, value, subtitle, icon: Icon, color = 'primary', index = 0 }) {
  const gradients = {
    primary: 'from-primary-800 to-primary-500',
    accent: 'from-accent-500 to-amber-400',
    success: 'from-emerald-500 to-teal-400',
    info: 'from-blue-500 to-cyan-400',
  }

  const glowColors = {
    primary: 'rgba(30, 58, 95, 0.12)',
    accent: 'rgba(245, 158, 11, 0.12)',
    success: 'rgba(16, 185, 129, 0.12)',
    info: 'rgba(59, 130, 246, 0.12)',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 30, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ delay: index * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className="liquid-glass p-6 group cursor-default"
    >
      {/* Colored glow orb */}
      <div
        className="absolute -top-8 -right-8 w-28 h-28 rounded-full opacity-60 group-hover:opacity-100 transition-opacity duration-700"
        style={{ background: `radial-gradient(circle, ${glowColors[color]}, transparent 70%)` }}
      />

      <div className="relative flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400">{title}</p>
          <p className="text-3xl font-black text-slate-800 dark:text-white tracking-tight">{value}</p>
          {subtitle && (
            <p className="text-sm text-slate-500 flex items-center gap-1.5">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              {subtitle}
            </p>
          )}
        </div>
        {Icon && (
          <div className={`p-3.5 rounded-2xl bg-gradient-to-br ${gradients[color]} shadow-lg group-hover:shadow-xl group-hover:scale-110 transition-all duration-300`}>
            <Icon className="w-5 h-5 text-white" />
          </div>
        )}
      </div>
    </motion.div>
  )
}
