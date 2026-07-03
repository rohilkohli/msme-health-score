import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, X, Send, Sparkles, User, Loader2 } from 'lucide-react'

const aiResponses = {
  score: "Your current composite score is **742/1000** (Good). This places you in the top 28% of MSMEs on our platform. Your strongest dimension is Compliance (88/100), while Growth Trajectory (65/100) has the most room for improvement.",
  improve: "Here are your top 3 actions to boost your score:\n\n1. **Diversify customers** — Your top client is 35% of revenue. Reducing to <25% could add +40 points.\n2. **Build cash reserves** — Maintain 3 months operating expenses. Impact: +30 points.\n3. **Accelerate collections** — Reduce receivables from 45 to 30 days. Impact: +25 points.",
  loan: "Based on your score of 742, you qualify for:\n\n• **MSME Business Loan** — Up to ₹1.5 Cr @ 10.5%\n• **Working Capital** — Up to ₹75L @ 11%\n• **Equipment Finance** — Up to ₹90L @ 9.5%\n\nYour ULI eligibility is **active**. I recommend applying for the Working Capital loan first.",
  compliance: "Your compliance score is **88/100** — excellent! All GST returns filed on time for 11 of the last 12 months. EPFO contributions are 95% on time. One suggestion: file GSTR-1 by the 10th (not 11th) to maintain a perfect record.",
  risk: "Current risk flags:\n\n⚠️ **Customer Concentration** — Top client is 35% of revenue\n⚠️ **Seasonal Cash Dip** — Q4 shows 20% lower inflows\n✅ No compliance risks\n✅ No balance deterioration\n\nOverall risk level: **Moderate (Low-Medium)**",
  default: "I'm your AI Financial Advisor. I can help you understand your health score, suggest improvements, check loan eligibility, or analyze your risk profile. Try asking:\n\n• \"How can I improve my score?\"\n• \"What loans am I eligible for?\"\n• \"Explain my risk factors\"\n• \"How is my compliance?\"",
}

function getAIResponse(message) {
  const lower = message.toLowerCase()
  if (lower.includes('score') && (lower.includes('what') || lower.includes('my') || lower.includes('current'))) return aiResponses.score
  if (lower.includes('improve') || lower.includes('increase') || lower.includes('boost') || lower.includes('better')) return aiResponses.improve
  if (lower.includes('loan') || lower.includes('credit') || lower.includes('borrow') || lower.includes('eligible')) return aiResponses.loan
  if (lower.includes('compliance') || lower.includes('gst') || lower.includes('epfo') || lower.includes('tax')) return aiResponses.compliance
  if (lower.includes('risk') || lower.includes('flag') || lower.includes('warning') || lower.includes('danger')) return aiResponses.risk
  return aiResponses.default
}

export default function AIAdvisor() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'ai', text: "Hello! I'm your AI Financial Advisor. Ask me anything about your MSME health score, improvement strategies, or loan eligibility." }
  ])
  const [input, setInput] = useState('')
  const [typing, setTyping] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userMsg }])
    setTyping(true)

    await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000))

    const response = getAIResponse(userMsg)
    setTyping(false)
    setMessages(prev => [...prev, { role: 'ai', text: response }])
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Floating Button */}
      <motion.button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 z-40 w-14 h-14 rounded-full bg-gradient-to-br from-accent-500 to-accent-600 text-white shadow-xl shadow-accent-500/30 flex items-center justify-center hover:scale-110 transition-transform ${isOpen ? 'hidden' : ''}`}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: 'spring' }}
      >
        <Sparkles className="w-6 h-6" />
      </motion.button>

      {/* Chat Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed bottom-6 right-6 z-50 w-[380px] h-[520px] liquid-glass-dark flex flex-col overflow-hidden"
            style={{ borderRadius: '24px' }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/[0.06]">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-accent-400 to-accent-600 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-white font-semibold text-sm">AI Advisor</h3>
                  <p className="text-emerald-400 text-[11px] flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
                    Online
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X className="w-4 h-4 text-white/60" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-2.5 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.role === 'ai' ? 'bg-accent-500/20' : 'bg-primary-500/20'
                  }`}>
                    {msg.role === 'ai' ? <Bot className="w-4 h-4 text-accent-400" /> : <User className="w-4 h-4 text-primary-300" />}
                  </div>
                  <div className={`max-w-[75%] px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
                    msg.role === 'ai'
                      ? 'bg-white/[0.06] text-white/90 rounded-tl-sm'
                      : 'bg-primary-600/40 text-white rounded-tr-sm'
                  }`}>
                    {msg.text.split('**').map((part, j) =>
                      j % 2 === 1 ? <strong key={j} className="text-accent-300">{part}</strong> : part
                    )}
                  </div>
                </motion.div>
              ))}
              {typing && (
                <div className="flex gap-2.5">
                  <div className="w-7 h-7 rounded-full bg-accent-500/20 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-accent-400" />
                  </div>
                  <div className="bg-white/[0.06] px-4 py-3 rounded-2xl rounded-tl-sm">
                    <Loader2 className="w-4 h-4 text-white/50 animate-spin" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-3 border-t border-white/[0.06]">
              <div className="flex items-center gap-2 bg-white/[0.06] rounded-xl px-3 py-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about your score..."
                  className="flex-1 bg-transparent text-white text-sm outline-none placeholder:text-white/30"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim()}
                  className="p-2 rounded-lg bg-accent-500 text-white disabled:opacity-30 hover:bg-accent-600 transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
              <p className="text-[10px] text-white/30 text-center mt-2">Powered by AI • Responses are advisory only</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
