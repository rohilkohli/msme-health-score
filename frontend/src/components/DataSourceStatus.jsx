import { CheckCircle2, Clock, XCircle, RefreshCw } from 'lucide-react'
import { formatRelativeTime } from '../utils/formatters'

export default function DataSourceStatus({ source, status, lastSync, onConnect }) {
  const statusConfig = {
    connected: {
      icon: CheckCircle2,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      label: 'Connected',
    },
    pending: {
      icon: Clock,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      label: 'Pending',
    },
    disconnected: {
      icon: XCircle,
      color: 'text-slate-400',
      bg: 'bg-slate-50',
      border: 'border-slate-200',
      label: 'Not Connected',
    },
  }

  const config = statusConfig[status] || statusConfig.disconnected
  const Icon = config.icon

  return (
    <div className={`flex items-center justify-between p-3 rounded-lg border ${config.border} ${config.bg}`}>
      <div className="flex items-center gap-3">
        <Icon className={`w-5 h-5 ${config.color}`} />
        <div>
          <p className="text-sm font-medium text-slate-700">{source}</p>
          {lastSync && (
            <p className="text-xs text-slate-500">Last sync: {formatRelativeTime(lastSync)}</p>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2">
        <span className={`text-xs font-semibold ${config.color}`}>{config.label}</span>
        {status === 'connected' && (
          <button className="p-1 rounded hover:bg-white/50 transition-colors">
            <RefreshCw className="w-3.5 h-3.5 text-slate-400" />
          </button>
        )}
        {status !== 'connected' && onConnect && (
          <button
            onClick={onConnect}
            className="text-xs bg-primary-800 text-white px-3 py-1 rounded-md hover:bg-primary-700 transition-colors"
          >
            Connect
          </button>
        )}
      </div>
    </div>
  )
}
