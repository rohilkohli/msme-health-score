import { useState, useEffect } from 'react'
import api from '../api/axios'

// Mock data for demonstration when backend is not available
const mockHealthScore = {
  composite_score: 742,
  category: 'Good',
  dimensions: {
    revenue_stability: { score: 78, trend: 'up', label: 'Revenue Stability' },
    expense_management: { score: 65, trend: 'stable', label: 'Expense Management' },
    tax_compliance: { score: 92, trend: 'up', label: 'Tax Compliance' },
    workforce_stability: { score: 71, trend: 'down', label: 'Workforce Stability' },
    banking_behavior: { score: 85, trend: 'up', label: 'Banking Behavior' },
  },
  strengths: [
    'Consistent GST filing with zero delays',
    'Healthy bank balance maintained above threshold',
    'Diverse revenue streams across 4+ clients',
    'Regular UPI transaction patterns indicate steady business',
  ],
  weaknesses: [
    'High expense-to-revenue ratio in Q4',
    'Employee attrition rate above industry average',
    'Credit utilization approaching 75% limit',
  ],
  recommendations: [
    { text: 'Reduce operational expenses by 15% to improve margins', priority: 'high' },
    { text: 'Diversify client base to reduce revenue concentration risk', priority: 'medium' },
    { text: 'Implement employee retention programs', priority: 'medium' },
    { text: 'Consider refinancing high-interest debt', priority: 'low' },
  ],
  last_updated: '2026-07-02T14:30:00Z',
  data_sources: {
    gst: { status: 'connected', last_sync: '2026-07-02T10:00:00Z' },
    bank: { status: 'connected', last_sync: '2026-07-02T08:00:00Z' },
    upi: { status: 'connected', last_sync: '2026-07-01T22:00:00Z' },
    epfo: { status: 'pending', last_sync: null },
  },
}

const mockHistory = [
  { date: '2026-01', score: 680, category: 'Fair' },
  { date: '2026-02', score: 695, category: 'Fair' },
  { date: '2026-03', score: 710, category: 'Good' },
  { date: '2026-04', score: 705, category: 'Good' },
  { date: '2026-05', score: 728, category: 'Good' },
  { date: '2026-06', score: 735, category: 'Good' },
  { date: '2026-07', score: 742, category: 'Good' },
]

const mockCreditAssessment = {
  credit_readiness: 78,
  eligible_products: [
    { name: 'Working Capital Loan', limit: '25,00,000', interest: '10.5%', provider: 'IDBI Bank' },
    { name: 'Business Term Loan', limit: '50,00,000', interest: '11.2%', provider: 'IDBI Bank' },
    { name: 'Invoice Discounting', limit: '15,00,000', interest: '9.8%', provider: 'OCEN Partner' },
    { name: 'Equipment Finance', limit: '30,00,000', interest: '10.0%', provider: 'IDBI Bank' },
  ],
  industry_benchmark: {
    average_score: 650,
    top_quartile: 780,
    your_percentile: 72,
  },
  improvement_areas: [
    { area: 'Reduce debt-to-equity ratio', impact: '+45 points', effort: 'Medium' },
    { area: 'Maintain 6 months cash reserves', impact: '+30 points', effort: 'High' },
    { area: 'File GST returns on time for 6 months', impact: '+20 points', effort: 'Low' },
  ],
}

export function useHealthScore() {
  const [healthScore, setHealthScore] = useState(null)
  const [history, setHistory] = useState([])
  const [creditAssessment, setCreditAssessment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchHealthScore = async () => {
    try {
      setLoading(true)
      const response = await api.get('/health-score')
      setHealthScore(response.data)
    } catch (err) {
      // Use mock data when backend is not available
      setHealthScore(mockHealthScore)
    } finally {
      setLoading(false)
    }
  }

  const fetchHistory = async () => {
    try {
      const response = await api.get('/health-score/history')
      setHistory(response.data)
    } catch (err) {
      setHistory(mockHistory)
    }
  }

  const fetchCreditAssessment = async () => {
    try {
      const response = await api.get('/credit-assessment')
      setCreditAssessment(response.data)
    } catch (err) {
      setCreditAssessment(mockCreditAssessment)
    }
  }

  useEffect(() => {
    fetchHealthScore()
    fetchHistory()
    fetchCreditAssessment()
  }, [])

  return {
    healthScore,
    history,
    creditAssessment,
    loading,
    error,
    refetch: fetchHealthScore,
  }
}
