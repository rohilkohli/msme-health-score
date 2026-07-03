import { ShieldCheck, AlertTriangle, AlertOctagon } from 'lucide-react'

export default function RiskIndicator({ level = 'medium', size = 'md' }) {
  const config = {
    low: {
      icon: ShieldCheck,
      label: 'Low Risk',
      color: 'text-emerald-600',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
    },
    medium: {
      icon: AlertTriangle,
      label: 'Medium Risk',
      color: 'text-amber-600',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
    },
    high: {
      icon: AlertOctagon,
      label: 'High Risk',
      color: 'text-red-600',
      bg: 'bg-red-50',
      border: 'border-red-200',
    },
  }

  const sizeMap = {
    sm: { icon: 'w-3 h-3', text: 'text-xs', padding: 'px-2 py-0.5' },
    md: { icon: 'w-4 h-4', text: 'text-sm', padding: 'px-3 py-1' },
    lg: { icon: 'w-5 h-5', text: 'text-base', padding: 'px-4 py-2' },
  }

  const { icon: Icon, label, color, bg, border } = config[level] || config.medium
  const sizeClasses = sizeMap[size] || sizeMap.md

  return (
    <div
      className={`inline-flex items-center gap-1.5 ${sizeClasses.padding} ${bg} ${border} border rounded-full`}
    >
      <Icon className={`${sizeClasses.icon} ${color}`} />
      <span className={`${sizeClasses.text} ${color} font-medium`}>{label}</span>
    </div>
  )
}
