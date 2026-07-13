import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, X, Database, BarChart3, CreditCard, Heart, Sparkles } from 'lucide-react'

const steps = [
  {
    icon: Sparkles,
    title: 'Welcome to MSME Health Score!',
    description: 'Your AI-powered financial health assessment platform. Let us guide you through the key features.',
    color: 'from-accent-400 to-accent-600',
  },
  {
    icon: Database,
    title: 'Connect Your Data Sources',
    description: 'Link GST, UPI, EPFO, and bank data through secure Account Aggregator consent. Your data stays private.',
    color: 'from-blue-400 to-blue-600',
  },
  {
    icon: BarChart3,
    title: 'Get Your Health Score',
    description: 'Our AI analyzes 6 dimensions — Cashflow, Repayment, Activity, Transaction Quality, Compliance, and Resilience — to generate your score (0-1000).',
    color: 'from-emerald-400 to-emerald-600',
  },
  {
    icon: Heart,
    title: 'View Your Health Card',
    description: 'A visual dashboard showing strengths, weaknesses, and actionable recommendations to improve your financial health.',
    color: 'from-rose-400 to-rose-600',
  },
  {
    icon: CreditCard,
    title: 'Access Credit Instantly',
    description: 'Use your score to unlock pre-approved loans from IDBI Bank and OCEN partners. Better score = better rates.',
    color: 'from-violet-400 to-violet-600',
  },
]

export default function OnboardingTour() {
  const [show, setShow] = useState(false)
  const [step, setStep] = useState(0)

  useEffect(() => {
    const seen = localStorage.getItem('onboarding_seen')
    if (!seen) {
      setTimeout(() => setShow(true), 1500)
    }
  }, [])

  const handleFinish = () => {
    localStorage.setItem('onboarding_seen', 'true')
    setShow(false)
  }

  const handleNext = () => {
    if (step < steps.length - 1) {
      setStep(step + 1)
    } else {
      handleFinish()
    }
  }

  if (!show) return null

  const current = steps[step]
  const Icon = current.icon

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4"
      >
        <motion.div
          key={step}
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="liquid-glass w-full max-w-md p-8 text-center relative"
        >
          <button
            onClick={handleFinish}
            className="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors"
          >
            <X className="w-4 h-4 text-slate-400" />
          </button>

          {/* Icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
            className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${current.color} mx-auto flex items-center justify-center shadow-lg mb-6`}
          >
            <Icon className="w-10 h-10 text-white" />
          </motion.div>

          {/* Content */}
          <h2 className="text-xl font-bold text-slate-800 mb-3">{current.title}</h2>
          <p className="text-sm text-slate-500 leading-relaxed mb-8">{current.description}</p>

          {/* Progress dots */}
          <div className="flex items-center justify-center gap-2 mb-6">
            {steps.map((_, i) => (
              <div
                key={i}
                className={`h-2 rounded-full transition-all duration-300 ${
                  i === step ? 'w-8 bg-accent-500' : i < step ? 'w-2 bg-accent-300' : 'w-2 bg-slate-200'
                }`}
              />
            ))}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between">
            <button
              onClick={handleFinish}
              className="text-sm text-slate-400 hover:text-slate-600 font-medium"
            >
              Skip Tour
            </button>
            <button
              onClick={handleNext}
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-primary-800 to-primary-600 text-white font-medium text-sm hover:shadow-lg transition-all"
            >
              {step === steps.length - 1 ? "Let's Go!" : 'Next'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}
