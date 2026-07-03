export const SCORE_CATEGORIES = {
  EXCELLENT: { min: 800, max: 1000, label: 'Excellent', color: '#10b981', bgColor: '#d1fae5' },
  GOOD: { min: 600, max: 799, label: 'Good', color: '#3b82f6', bgColor: '#dbeafe' },
  FAIR: { min: 400, max: 599, label: 'Fair', color: '#f59e0b', bgColor: '#fef3c7' },
  POOR: { min: 200, max: 399, label: 'Needs Improvement', color: '#f97316', bgColor: '#fed7aa' },
  CRITICAL: { min: 0, max: 199, label: 'Critical', color: '#ef4444', bgColor: '#fee2e2' },
}

export const DIMENSIONS = [
  { key: 'revenue_stability', label: 'Revenue Stability', icon: 'TrendingUp', description: 'GST filing consistency, revenue growth trend, seasonal variance' },
  { key: 'cash_flow_health', label: 'Cash Flow Health', icon: 'Wallet', description: 'Inflow/outflow ratio, transaction regularity, working capital' },
  { key: 'compliance_score', label: 'Compliance Score', icon: 'FileCheck', description: 'GST + EPFO filing timeliness and statutory compliance' },
  { key: 'growth_trajectory', label: 'Growth Trajectory', icon: 'TrendingUp', description: 'Revenue CAGR, customer base growth, workforce expansion' },
  { key: 'repayment_capacity', label: 'Repayment Capacity', icon: 'Building', description: 'DSCR, free cash flow, obligation coverage ratio' },
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
  if (score >= 600) return SCORE_CATEGORIES.GOOD
  if (score >= 400) return SCORE_CATEGORIES.FAIR
  if (score >= 200) return SCORE_CATEGORIES.POOR
  return SCORE_CATEGORIES.CRITICAL
}

export function getScoreColor(score) {
  return getScoreCategory(score).color
}
