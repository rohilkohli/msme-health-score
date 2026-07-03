import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, CheckCircle2, ArrowRight, IndianRupee, Clock, Shield, FileText } from 'lucide-react'
import toast from 'react-hot-toast'

export default function LoanApplicationModal({ product, onClose }) {
  const [step, setStep] = useState(1)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async () => {
    setSubmitting(true)
    await new Promise(r => setTimeout(r, 2000))
    setSubmitting(false)
    setStep(3)
    toast.success('Application submitted successfully!')
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95 }}
        onClick={(e) => e.stopPropagation()}
        className="liquid-glass w-full max-w-md overflow-hidden"
      >
        {/* Header */}
        <div className="gradient-primary p-5 relative">
          <button onClick={onClose} className="absolute top-4 right-4 p-1.5 rounded-full bg-white/10 hover:bg-white/20">
            <X className="w-4 h-4 text-white" />
          </button>
          <p className="text-primary-200 text-xs font-medium">Loan Application</p>
          <h3 className="text-white font-bold text-lg mt-1">{product?.name || 'MSME Business Loan'}</h3>
          <div className="flex items-center gap-4 mt-3">
            <div className="flex items-center gap-1 text-accent-300 text-sm">
              <IndianRupee className="w-3.5 h-3.5" />
              <span className="font-bold">{product?.max_amount || '₹ 1.5 Cr'}</span>
            </div>
            <div className="flex items-center gap-1 text-primary-200 text-sm">
              <Clock className="w-3.5 h-3.5" />
              <span>{product?.tenure || '12-60 months'}</span>
            </div>
          </div>
        </div>

        <div className="p-6">
          {/* Step indicator */}
          <div className="flex items-center gap-2 mb-6">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center gap-2 flex-1">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                  step >= s ? 'bg-primary-800 text-white' : 'bg-slate-100 text-slate-400'
                }`}>
                  {step > s ? <CheckCircle2 className="w-4 h-4" /> : s}
                </div>
                {s < 3 && <div className={`flex-1 h-0.5 rounded ${step > s ? 'bg-primary-800' : 'bg-slate-200'}`} />}
              </div>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.div key="step1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                <h4 className="font-semibold text-slate-800 mb-4">Pre-filled from Health Score</h4>
                <div className="space-y-3 bg-slate-50 rounded-xl p-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">Business Name</span>
                    <span className="font-medium text-slate-800">Sri Lakshmi Textiles</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">GSTIN</span>
                    <span className="font-medium text-slate-800 font-mono">27AABCS1234A1Z5</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">Health Score</span>
                    <span className="font-bold text-emerald-600">742 (Good)</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">Annual Turnover</span>
                    <span className="font-medium text-slate-800">₹ 2.5 Cr</span>
                  </div>
                </div>
                <div className="flex items-start gap-2 mt-4 p-3 bg-emerald-50 rounded-lg">
                  <Shield className="w-4 h-4 text-emerald-600 mt-0.5" />
                  <p className="text-xs text-emerald-700">Your data is auto-filled from verified sources via Account Aggregator. No manual documents needed.</p>
                </div>
                <button onClick={() => setStep(2)} className="w-full mt-6 flex items-center justify-center gap-2 bg-primary-800 text-white py-3 rounded-xl font-medium hover:bg-primary-700 transition-colors">
                  Continue <ArrowRight className="w-4 h-4" />
                </button>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div key="step2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                <h4 className="font-semibold text-slate-800 mb-4">Loan Details</h4>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1 block">Loan Amount Required</label>
                    <div className="relative">
                      <IndianRupee className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input type="text" defaultValue="25,00,000" className="w-full pl-9 pr-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:border-primary-800 focus:ring-2 focus:ring-primary-800/20 outline-none" />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1 block">Purpose</label>
                    <select className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:border-primary-800 outline-none">
                      <option>Working Capital</option>
                      <option>Equipment Purchase</option>
                      <option>Business Expansion</option>
                      <option>Inventory Finance</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1 block">Preferred Tenure</label>
                    <select className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm focus:border-primary-800 outline-none">
                      <option>12 months</option>
                      <option>24 months</option>
                      <option>36 months</option>
                      <option>48 months</option>
                    </select>
                  </div>
                </div>
                <div className="flex gap-3 mt-6">
                  <button onClick={() => setStep(1)} className="flex-1 py-2.5 rounded-xl border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 text-sm">Back</button>
                  <button onClick={handleSubmit} disabled={submitting} className="flex-1 py-2.5 rounded-xl bg-primary-800 text-white font-medium hover:bg-primary-700 text-sm disabled:opacity-50 flex items-center justify-center gap-2">
                    {submitting ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <><FileText className="w-4 h-4" /> Submit</>}
                  </button>
                </div>
              </motion.div>
            )}

            {step === 3 && (
              <motion.div key="step3" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-4">
                <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 className="w-8 h-8 text-emerald-600" />
                </div>
                <h4 className="text-lg font-bold text-slate-800">Application Submitted!</h4>
                <p className="text-sm text-slate-500 mt-2 mb-6">Your loan application has been sent to IDBI Bank via ULI. Expected response within 24 hours.</p>
                <div className="bg-slate-50 rounded-xl p-4 text-left space-y-2 mb-6">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">Application ID</span>
                    <span className="font-mono font-bold text-slate-800">IDBI-2026-{Math.random().toString(36).slice(2, 8).toUpperCase()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-500">Status</span>
                    <span className="font-medium text-amber-600">Under Review</span>
                  </div>
                </div>
                <button onClick={onClose} className="w-full py-3 rounded-xl bg-primary-800 text-white font-medium hover:bg-primary-700">
                  Done
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  )
}
