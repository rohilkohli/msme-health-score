import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  FileText,
  Building,
  Smartphone,
  Users,
  CheckCircle2,
  Clock,
  XCircle,
  Shield,
  ArrowRight,
  RefreshCw,
  Link2,
  AlertTriangle,
} from 'lucide-react'
import toast from 'react-hot-toast'

const dataSources = [
  {
    id: 'gst',
    name: 'GST Portal',
    description: 'Tax filing history, returns data, and compliance records from GSTN',
    icon: FileText,
    color: 'bg-blue-500',
    fields: ['GSTR-1', 'GSTR-3B', 'Tax Payments', 'Filing History'],
    status: 'connected',
    lastSync: '2026-07-02T10:00:00Z',
  },
  {
    id: 'bank',
    name: 'Bank Statements',
    description: 'Transaction history and account details via Account Aggregator (AA)',
    icon: Building,
    color: 'bg-emerald-500',
    fields: ['Current Account', 'Savings Account', 'Loan Accounts', 'FD/RD'],
    status: 'connected',
    lastSync: '2026-07-02T08:00:00Z',
  },
  {
    id: 'upi',
    name: 'UPI Transactions',
    description: 'Digital payment patterns and transaction frequency analysis',
    icon: Smartphone,
    color: 'bg-purple-500',
    fields: ['Payment Received', 'Payments Made', 'Frequency', 'Patterns'],
    status: 'pending',
    lastSync: null,
  },
  {
    id: 'epfo',
    name: 'EPFO Data',
    description: 'Employee provident fund compliance and workforce data',
    icon: Users,
    color: 'bg-orange-500',
    fields: ['Employee Count', 'Contribution History', 'Compliance Status', 'Challan Data'],
    status: 'disconnected',
    lastSync: null,
  },
]

export default function DataConnect() {
  const [sources, setSources] = useState(dataSources)
  const [connecting, setConnecting] = useState(null)
  const [showConsent, setShowConsent] = useState(false)
  const [consentSource, setConsentSource] = useState(null)

  const getStatusConfig = (status) => {
    switch (status) {
      case 'connected':
        return { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50', label: 'Connected' }
      case 'pending':
        return { icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50', label: 'Pending Consent' }
      default:
        return { icon: XCircle, color: 'text-slate-400', bg: 'bg-slate-50', label: 'Not Connected' }
    }
  }

  const handleConnect = (source) => {
    setConsentSource(source)
    setShowConsent(true)
  }

  const handleGrantConsent = async () => {
    if (!consentSource) return
    setShowConsent(false)
    setConnecting(consentSource.id)

    // Simulate connection process
    await new Promise(resolve => setTimeout(resolve, 2000))

    setSources(prev =>
      prev.map(s =>
        s.id === consentSource.id
          ? { ...s, status: 'connected', lastSync: new Date().toISOString() }
          : s
      )
    )
    setConnecting(null)
    toast.success(`${consentSource.name} connected successfully!`)
  }

  const connectedCount = sources.filter(s => s.status === 'connected').length
  const progressPercent = (connectedCount / sources.length) * 100

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Connect Data Sources</h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
          Link your financial data through Account Aggregator for a comprehensive health assessment
        </p>
      </div>

      {/* Progress */}
      <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Link2 className="w-5 h-5 text-primary-800" />
            <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
              Data Connection Progress
            </span>
          </div>
          <span className="text-sm font-bold text-primary-800">{connectedCount}/{sources.length} Connected</span>
        </div>
        <div className="w-full h-3 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-primary-800 to-accent-500 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercent}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>
        <p className="text-xs text-slate-500 mt-2">
          Connect all sources for the most accurate health score assessment
        </p>
      </div>

      {/* AA Information */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800 flex items-start gap-3">
        <Shield className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
        <div>
          <p className="text-sm font-medium text-blue-800 dark:text-blue-200">
            Account Aggregator Framework
          </p>
          <p className="text-xs text-blue-600 dark:text-blue-300 mt-1">
            Your data is fetched securely through RBI-regulated Account Aggregators.
            You control what data is shared and can revoke consent at any time.
          </p>
        </div>
      </div>

      {/* Data Source Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sources.map((source, index) => {
          const status = getStatusConfig(source.status)
          const StatusIcon = status.icon
          const isConnecting = connecting === source.id

          return (
            <motion.div
              key={source.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 ${source.color} rounded-xl flex items-center justify-center`}>
                    <source.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-800 dark:text-white">{source.name}</h3>
                    <div className={`flex items-center gap-1 mt-0.5 ${status.color}`}>
                      <StatusIcon className="w-3.5 h-3.5" />
                      <span className="text-xs font-medium">{status.label}</span>
                    </div>
                  </div>
                </div>
              </div>

              <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
                {source.description}
              </p>

              <div className="flex flex-wrap gap-2 mb-4">
                {source.fields.map((field, i) => (
                  <span
                    key={i}
                    className="text-xs bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 px-2 py-1 rounded-md"
                  >
                    {field}
                  </span>
                ))}
              </div>

              {source.status === 'connected' ? (
                <div className="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-slate-700">
                  <span className="text-xs text-slate-500">
                    Last synced: {new Date(source.lastSync).toLocaleString('en-IN')}
                  </span>
                  <button className="flex items-center gap-1 text-xs text-primary-800 font-medium hover:underline">
                    <RefreshCw className="w-3 h-3" />
                    Re-sync
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => handleConnect(source)}
                  disabled={isConnecting}
                  className="w-full flex items-center justify-center gap-2 bg-primary-800 text-white py-2.5 rounded-lg font-medium text-sm hover:bg-primary-700 transition-colors disabled:opacity-50"
                >
                  {isConnecting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Connecting...
                    </>
                  ) : (
                    <>
                      Connect via AA
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              )}
            </motion.div>
          )
        })}
      </div>

      {/* Consent Modal */}
      {showConsent && consentSource && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-slate-800 rounded-2xl p-6 max-w-md w-full shadow-2xl"
          >
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-8 h-8 text-primary-800" />
              </div>
              <h3 className="text-xl font-bold text-slate-800 dark:text-white">
                Consent Request
              </h3>
              <p className="text-sm text-slate-500 mt-2">
                Grant consent to access your {consentSource.name} data
              </p>
            </div>

            <div className="bg-slate-50 dark:bg-slate-700 rounded-lg p-4 mb-4">
              <p className="text-xs font-medium text-slate-600 dark:text-slate-300 mb-2">Data to be accessed:</p>
              <ul className="space-y-1">
                {consentSource.fields.map((field, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-200">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    {field}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3 mb-6 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 mt-0.5" />
              <p className="text-xs text-amber-700 dark:text-amber-200">
                This consent is valid for 6 months. You can revoke it anytime from this page.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowConsent(false)}
                className="flex-1 py-2.5 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 transition-colors text-sm"
              >
                Deny
              </button>
              <button
                onClick={handleGrantConsent}
                className="flex-1 py-2.5 rounded-lg bg-primary-800 text-white font-medium hover:bg-primary-700 transition-colors text-sm"
              >
                Grant Consent
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </motion.div>
  )
}
