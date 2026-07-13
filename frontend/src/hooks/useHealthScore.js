import { useState, useEffect } from 'react'
import api from '../api/axios'

const mockHealthScore = {
  composite_score: 742,
  category: 'Strong',
  risk_level: 'Moderate',
  dimensions: {
    cashflow_strength_stability: { score: 78, trend: 'up', label: 'Cashflow Strength & Stability', weight: 0.25, weighted_score: 19.5, sub_metrics: {}, insights: [] },
    repayment_capacity_leverage: { score: 72, trend: 'up', label: 'Repayment Capacity & Leverage', weight: 0.20, weighted_score: 14.4, sub_metrics: {}, insights: [] },
    business_activity_growth: { score: 74, trend: 'up', label: 'Business Activity & Growth', weight: 0.15, weighted_score: 11.1, sub_metrics: {}, insights: [] },
    transaction_quality_conduct: { score: 68, trend: 'stable', label: 'Transaction Quality & Conduct', weight: 0.15, weighted_score: 10.2, sub_metrics: {}, insights: [] },
    compliance_formalization: { score: 82, trend: 'up', label: 'Compliance & Formalization', weight: 0.15, weighted_score: 12.3, sub_metrics: {}, insights: [] },
    resilience_risk_buffers: { score: 70, trend: 'stable', label: 'Resilience & Risk Buffers', weight: 0.10, weighted_score: 7.0, sub_metrics: {}, insights: [] },
  },
  top_strengths: [
    'Consistent GST filing with zero delays in last 12 months',
    'Healthy bank balance maintained above 2x monthly obligations',
    'Diverse revenue streams across 4+ client segments',
  ],
  top_risks: [
    'Cash flow shows pressure in Q4 due to seasonal dip',
    'Growth trajectory below industry average of 15% CAGR',
    'High customer concentration — top client is 35% of revenue',
  ],
  recommendations: [
    { text: 'Diversify client base to reduce revenue concentration below 25%', priority: 'high' },
    { text: 'Build cash reserves for 3 months of operating expenses', priority: 'high' },
    { text: 'Explore new market segments to accelerate growth trajectory', priority: 'medium' },
    { text: 'Consider seasonal credit line for Q4 cash flow management', priority: 'low' },
  ],
  ml_prediction_score: 76.4,
  computed_at: '2026-07-02T14:30:00Z',
}

const mockHistory = [
  { date: '2026-01', score: 680, category: 'Good' },
  { date: '2026-02', score: 695, category: 'Good' },
  { date: '2026-03', score: 710, category: 'Good' },
  { date: '2026-04', score: 705, category: 'Good' },
  { date: '2026-05', score: 728, category: 'Good' },
  { date: '2026-06', score: 735, category: 'Good' },
  { date: '2026-07', score: 742, category: 'Good' },
]

export function useHealthScore() {
  const [healthScore, setHealthScore] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchHealthScore = async () => {
    try {
      setLoading(true)
      const msmeRes = await api.get('/msme/list')
      if (msmeRes.data && msmeRes.data.length > 0) {
        const msmeId = msmeRes.data[0].id
        const response = await api.get(`/health-score/${msmeId}`)
        const data = response.data
        // Normalize dimension labels
        const dims = {}
        for (const [key, val] of Object.entries(data.dimensions || {})) {
          const labels = {
            cashflow_strength_stability: 'Cashflow Strength & Stability',
            repayment_capacity_leverage: 'Repayment Capacity & Leverage',
            business_activity_growth: 'Business Activity & Growth',
            transaction_quality_conduct: 'Transaction Quality & Conduct',
            compliance_formalization: 'Compliance & Formalization',
            resilience_risk_buffers: 'Resilience & Risk Buffers',
          }
          const trend = val.trend_3m || val.trend_6m || val.trend_12m || 'stable'
          dims[key] = { ...val, label: labels[key] || val.label || key, trend }
        }
        // Derive strengths/weaknesses from dimension scores
        const strengths = [...(data.top_strengths || [])]
        const weaknesses = [...(data.top_risks || [])]
        for (const [, val] of Object.entries(dims)) {
          if (val.score >= 75) strengths.push(`Strong ${val.label.toLowerCase()} performance (${Math.round(val.score)}/100)`)
          else if (val.score < 50) weaknesses.push(`${val.label} needs attention (${Math.round(val.score)}/100)`)
        }
        if (strengths.length === 0) strengths.push('Business operational with active data sources')
        if (weaknesses.length === 0) weaknesses.push('No major concerns identified')

        setHealthScore({ ...data, dimensions: dims, strengths, weaknesses, computed_at: data.computed_at })
      } else {
        setHealthScore(mockHealthScore)
      }
    } catch {
      setHealthScore(mockHealthScore)
    } finally {
      setLoading(false)
    }
  }

  const fetchHistory = async () => {
    try {
      const msmeRes = await api.get('/msme/list')
      if (msmeRes.data && msmeRes.data.length > 0) {
        const res = await api.get(`/health-score/${msmeRes.data[0].id}/history`)
        if (res.data.scores && res.data.scores.length > 0) {
          setHistory(res.data.scores.map(s => ({
            date: s.computed_at ? new Date(s.computed_at).toLocaleDateString('en-IN', { month: 'short', year: '2-digit' }) : '',
            score: s.composite_score,
            category: s.category,
          })))
          return
        }
      }
      setHistory(mockHistory)
    } catch {
      setHistory(mockHistory)
    }
  }

  const mockCreditAssessment = {
    credit_readiness: 78,
    eligible_products: [
      { name: 'Working Capital Loan', limit: '₹25,00,000', interest: '10.5%', provider: 'IDBI Bank' },
      { name: 'Business Term Loan', limit: '₹50,00,000', interest: '11.2%', provider: 'IDBI Bank' },
      { name: 'Invoice Discounting', limit: '₹15,00,000', interest: '9.8%', provider: 'OCEN Partner' },
      { name: 'Equipment Finance', limit: '₹30,00,000', interest: '10.0%', provider: 'IDBI Bank' },
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

  useEffect(() => {
    fetchHealthScore()
    fetchHistory()
  }, [])

  return {
    healthScore,
    history,
    creditAssessment: mockCreditAssessment,
    loading,
    refetch: fetchHealthScore,
  }
}
