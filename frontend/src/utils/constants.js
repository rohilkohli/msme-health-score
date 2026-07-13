export const SCORE_CATEGORIES = {
  VERY_STRONG: { min: 800, max: 1000, label: 'Very Strong', color: '#10b981', bgColor: '#d1fae5' },
  STRONG: { min: 700, max: 799, label: 'Strong', color: '#3b82f6', bgColor: '#dbeafe' },
  MODERATE: { min: 600, max: 699, label: 'Moderate', color: '#f59e0b', bgColor: '#fef3c7' },
  WEAK: { min: 500, max: 599, label: 'Weak', color: '#f97316', bgColor: '#fed7aa' },
  HIGH_RISK: { min: 0, max: 499, label: 'High Risk', color: '#ef4444', bgColor: '#fee2e2' },
}

export const DIMENSIONS = [
  { key: 'cashflow_strength_stability', label: 'Cashflow Strength & Stability', icon: 'Wallet', description: 'AA bank flows, GST sales trend, UPI inflow consistency' },
  { key: 'repayment_capacity_leverage', label: 'Repayment Capacity & Leverage', icon: 'Building', description: 'Debt servicing ability, obligation coverage, leverage proxy' },
  { key: 'business_activity_growth', label: 'Business Activity & Growth', icon: 'TrendingUp', description: 'GST filing regularity, invoice momentum, growth trend' },
  { key: 'transaction_quality_conduct', label: 'Transaction Quality & Conduct', icon: 'FileCheck', description: 'Anomaly control, concentration risk, transaction discipline' },
  { key: 'compliance_formalization', label: 'Compliance & Formalization', icon: 'FileCheck', description: 'GST/EPFO timeliness, continuity, business vintage' },
  { key: 'resilience_risk_buffers', label: 'Resilience & Risk Buffers', icon: 'ShieldCheck', description: 'Liquidity buffer, volatility stress, adverse event control' },
]

export const DATA_SOURCES = [
  { key: 'gst', label: 'GST Portal', description: 'Tax filing and compliance data', icon: 'FileText' },
  { key: 'bank', label: 'Bank Statements', description: 'Transaction history via Account Aggregator', icon: 'Building' },
  { key: 'upi', label: 'UPI Transactions', description: 'Digital payment patterns', icon: 'Smartphone' },
  { key: 'epfo', label: 'EPFO', description: 'Employee provident fund data', icon: 'Users' },
]

export const RISK_LEVELS = {
  LOW: { label: 'Low Risk', color: '#10b981', icon: 'ShieldCheck' },
  MEDIUM: { label: 'Medium Risk', color: '#f59e0b', icon: 'AlertTriangle' },
  HIGH: { label: 'High Risk', color: '#ef4444', icon: 'AlertOctagon' },
}

export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: 'LayoutDashboard' },
  { path: '/health-card', label: 'Health Card', icon: 'Heart' },
  { path: '/data-connect', label: 'Data Sources', icon: 'Database' },
  { path: '/credit-assessment', label: 'Credit Assessment', icon: 'CreditCard' },
  { path: '/history', label: 'Score History', icon: 'History' },
  { path: '/msme-register', label: 'Business Profile', icon: 'Building2' },
]

export function getScoreCategory(score) {
  if (score >= 800) return SCORE_CATEGORIES.VERY_STRONG
  if (score >= 700) return SCORE_CATEGORIES.STRONG
  if (score >= 600) return SCORE_CATEGORIES.MODERATE
  if (score >= 500) return SCORE_CATEGORIES.WEAK
  return SCORE_CATEGORIES.HIGH_RISK
}

export function getScoreColor(score) {
  return getScoreCategory(score).color
}
