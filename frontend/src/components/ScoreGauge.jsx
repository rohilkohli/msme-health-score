import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { getScoreCategory } from '../utils/constants'

export default function ScoreGauge({ score = 0, maxScore = 1000, size = 240 }) {
  const [animatedScore, setAnimatedScore] = useState(0)
  const category = getScoreCategory(score)
  const percentage = (score / maxScore) * 100
  const radius = (size - 30) / 2
  const circumference = 2 * Math.PI * radius

  useEffect(() => {
    const duration = 2000
    const steps = 80
    const increment = score / steps
    let current = 0
    const timer = setInterval(() => {
      current += increment
      if (current >= score) {
        setAnimatedScore(score)
        clearInterval(timer)
      } else {
        setAnimatedScore(Math.round(current))
      }
    }, duration / steps)
    return () => clearInterval(timer)
  }, [score])

  const strokeDashoffset = circumference - (percentage / 100) * circumference * 0.75
  const rotation = 135

  return (
    <div className="relative inline-flex items-center justify-center">
      {/* Outer glow ring */}
      <div
        className="absolute rounded-full animate-pulse-ring"
        style={{
          width: size + 20,
          height: size + 20,
          background: `radial-gradient(circle, ${category.color}15 0%, transparent 70%)`,
        }}
      />

      <svg width={size} height={size} className="drop-shadow-lg" style={{ transform: `rotate(${rotation}deg)` }}>
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(226, 232, 240, 0.4)"
          strokeWidth="14"
          fill="none"
          strokeDasharray={circumference * 0.75}
          strokeLinecap="round"
        />
        {/* Score arc with gradient */}
        <defs>
          <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={category.color} stopOpacity="0.8" />
            <stop offset="100%" stopColor={category.color} />
          </linearGradient>
        </defs>
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="url(#scoreGrad)"
          strokeWidth="14"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference * 0.75}
          initial={{ strokeDashoffset: circumference * 0.75 }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 2, ease: [0.22, 1, 0.36, 1] }}
        />
        {/* Glow duplicate */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={category.color}
          strokeWidth="14"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference * 0.75}
          initial={{ strokeDashoffset: circumference * 0.75 }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 2, ease: [0.22, 1, 0.36, 1] }}
          opacity="0.2"
          filter="blur(6px)"
        />
      </svg>

      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className="text-5xl md:text-6xl font-black tracking-tight"
          style={{ color: category.color }}
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          {animatedScore}
        </motion.span>
        <span className="text-white/60 text-xs mt-1 font-medium tracking-wide">out of {maxScore}</span>
        <motion.div
          className="mt-3 px-4 py-1.5 rounded-full text-xs font-bold text-white shadow-lg"
          style={{ backgroundColor: category.color, boxShadow: `0 4px 14px ${category.color}40` }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.4 }}
        >
          {category.label}
        </motion.div>
      </div>
    </div>
  )
}
