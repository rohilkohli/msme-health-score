import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Activity,
  Shield,
  Zap,
  Brain,
  Lock,
  Globe,
  ArrowRight,
  CheckCircle2,
  UserPlus,
  Database,
  BarChart3,
  CreditCard,
  Star,
  TrendingUp,
} from 'lucide-react'

const features = [
  { icon: Zap, title: 'Real-time Scoring', description: 'Instant financial health assessment updated with every transaction' },
  { icon: Database, title: 'Multi-source Data', description: 'Aggregates GST, UPI, EPFO, and bank data for holistic analysis' },
  { icon: Brain, title: 'Explainable AI', description: 'Transparent scoring with clear reasoning behind every dimension' },
  { icon: Globe, title: 'ULI/OCEN Ready', description: 'Built on India Stack protocols for seamless lending integration' },
  { icon: Lock, title: 'Privacy-first (AA)', description: 'Account Aggregator framework ensures data consent and security' },
  { icon: Activity, title: 'Instant Assessment', description: 'Get your complete financial health card in under 60 seconds' },
]

const steps = [
  { number: '01', icon: UserPlus, title: 'Register', description: 'Create your account and register your MSME business details' },
  { number: '02', icon: Database, title: 'Connect Data', description: 'Link your financial data sources through secure AA consent' },
  { number: '03', icon: BarChart3, title: 'Get Score', description: 'AI analyzes your data across 6 multidimensional financial dimensions' },
  { number: '04', icon: CreditCard, title: 'Access Credit', description: 'Use your health score to unlock pre-approved credit offers' },
]

const stats = [
  { value: '50,000+', label: 'MSMEs Assessed' },
  { value: '₹2,400 Cr', label: 'Credit Facilitated' },
  { value: '< 60 sec', label: 'Assessment Time' },
  { value: '99.9%', label: 'Data Security' },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-primary-800 rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-primary-800 text-lg">MSME Health Score</span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                to="/login"
                className="text-sm font-medium text-slate-600 hover:text-primary-800 transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="text-sm font-medium bg-primary-800 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-50/50 to-transparent"></div>
        <div className="absolute top-20 left-10 w-72 h-72 bg-accent-200/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-primary-200/20 rounded-full blur-3xl"></div>

        <div className="max-w-7xl mx-auto relative">
          <div className="text-center max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center gap-2 bg-accent-50 border border-accent-200 rounded-full px-4 py-1.5 mb-6">
                <Star className="w-4 h-4 text-accent-500" />
                <span className="text-sm font-medium text-accent-700">IDBI Innovate 2026</span>
              </div>
            </motion.div>

            <motion.h1
              className="text-4xl md:text-6xl lg:text-7xl font-bold text-primary-800 leading-tight"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              MSME Financial
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-500 to-accent-600">
                Health Score
              </span>
            </motion.h1>

            <motion.p
              className="mt-6 text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              AI-Powered Credit Assessment for India's Backbone. Transform your financial data
              into actionable insights and unlock access to credit.
            </motion.p>

            <motion.div
              className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Link
                to="/register"
                className="group flex items-center gap-2 bg-primary-800 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-primary-700 transition-all shadow-lg shadow-primary-800/25 hover:shadow-xl"
              >
                Get Your Score
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <button
                onClick={() => {
                  localStorage.setItem('auth_token', 'demo_token_123')
                  localStorage.setItem('user', JSON.stringify({ id: 1, name: 'Demo User', email: 'demo@idbihealthscore.in' }))
                  window.location.href = '/dashboard'
                }}
                className="flex items-center gap-2 bg-white text-primary-800 px-8 py-4 rounded-xl font-semibold text-lg border-2 border-primary-200 hover:border-primary-800 transition-all cursor-pointer"
              >
                View Demo
              </button>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <p className="text-2xl md:text-3xl font-bold text-primary-800">{stat.value}</p>
                <p className="text-sm text-slate-500 mt-1">{stat.label}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-slate-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-primary-800">
              Why Choose MSME Health Score?
            </h2>
            <p className="mt-4 text-lg text-slate-600 max-w-2xl mx-auto">
              Built on India's digital public infrastructure, delivering transparent and
              comprehensive financial assessment
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                className="bg-white rounded-xl p-6 border border-slate-200 hover:shadow-xl hover:border-primary-200 transition-all group"
              >
                <div className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary-800 transition-colors">
                  <feature.icon className="w-6 h-6 text-primary-800 group-hover:text-white transition-colors" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-500 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-primary-800">
              How It Works
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              Four simple steps to your financial health score
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.15, duration: 0.5 }}
                className="text-center relative"
              >
                {index < 3 && (
                  <div className="hidden lg:block absolute top-12 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-primary-200 to-transparent"></div>
                )}
                <div className="relative inline-flex items-center justify-center mb-4">
                  <div className="w-24 h-24 bg-primary-50 rounded-full flex items-center justify-center">
                    <step.icon className="w-10 h-10 text-primary-800" />
                  </div>
                  <span className="absolute -top-2 -right-2 w-8 h-8 bg-accent-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {step.number}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">{step.title}</h3>
                <p className="text-sm text-slate-500">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Score Dimensions */}
      <section className="py-20 px-4 bg-primary-800">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white">
              5 Dimensions of Financial Health
            </h2>
            <p className="mt-4 text-lg text-primary-200">
              A comprehensive multidimensional assessment of your business
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { label: 'Revenue Stability', icon: TrendingUp, score: '78/100' },
              { label: 'Expense Management', icon: BarChart3, score: '65/100' },
              { label: 'Tax Compliance', icon: Shield, score: '92/100' },
              { label: 'Workforce Stability', icon: UserPlus, score: '71/100' },
              { label: 'Banking Behavior', icon: CreditCard, score: '85/100' },
            ].map((dim, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur border border-white/20 rounded-xl p-5 text-center hover:bg-white/20 transition-colors"
              >
                <dim.icon className="w-8 h-8 text-accent-400 mx-auto mb-3" />
                <h4 className="text-white font-semibold text-sm mb-1">{dim.label}</h4>
                <p className="text-accent-300 font-bold text-lg">{dim.score}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-primary-800">
              Ready to Know Your Financial Health?
            </h2>
            <p className="mt-4 text-lg text-slate-600 mb-8">
              Join thousands of MSMEs already using our platform to improve their financial health
              and access better credit
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/register"
                className="group flex items-center gap-2 bg-accent-500 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-accent-600 transition-all shadow-lg shadow-accent-500/25"
              >
                Start Free Assessment
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
            <div className="mt-6 flex items-center justify-center gap-6 text-sm text-slate-500">
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> No credit card required
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Data encrypted end-to-end
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" /> RBI compliant
              </span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <div className="w-9 h-9 bg-accent-500 rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg">MSME Health Score</span>
            </div>
            <p className="text-slate-400 text-sm">
              Built for IDBI Innovate 2026 | Powered by Account Aggregator, ULI & OCEN
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
