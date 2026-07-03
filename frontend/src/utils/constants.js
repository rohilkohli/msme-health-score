export const SCORE_CATEGORIES = {
  EXCELLENT: { min: 800, max: 1000, label: 'Excellent', color: '#10b981', bgColor: '#d1fae5' },
  GOOD: { min: 650, max: 799, label: 'Good', color: '#3b82f6', bgColor: '#dbeafe' },
  FAIR: { min: 500, max: 649, label: 'Fair', color: '#f59e0b', bgColor: '#fef3c7' },
  POOR: { min: 350, max: 499, label: 'Poor', color: '#f97316', bgColor: '#fed7aa' },
  CRITICAL: { min: 0, max: 349, label: 'Critical', color: '#ef4444', bgColor: '#fee2e2' },
}

export const DIMENSIONS = [
  { key: 'revenue_stability', label: 'Revenue Stability', icon: 'TrendingUp', description: 'Consistency and growth of revenue streams' },
  { key: 'expense_management', label: 'Expense Management', icon: 'Wallet', description: 'Efficiency in managing business expenses' },
  { key: 'tax_compliance', label: 'Tax Compliance', icon: 'FileCheck', description: 'GST filing regularity and accuracy' },
  { key: 'workforce_stability', label: 'Workforce Stability', icon: 'Users', description: 'Employee retention and EPFO compliance' },
  { key: 'banking_behavior', label: 'Banking Behavior', icon: 'Building', description: 'Account health and transaction patterns' },
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
  if (score >= 800) return SCORE_CATEGORIES.EXCELLENT
  if (score >= 650) return SCORE_CATEGORIES.GOOD
  if (score >= 500) return SCORE_CATEGORIES.FAIR
  if (score >= 350) return SCORE_CATEGORIES.POOR
  return SCORE_CATEGORIES.CRITICAL
}

export function getScoreColor(score) {
  return getScoreCategory(score).color
}
