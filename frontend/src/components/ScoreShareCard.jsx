import { useState } from 'react'
import { motion } from 'framer-motion'
import { Share2, Copy, CheckCircle2, Download, Link2, QrCode } from 'lucide-react'
import toast from 'react-hot-toast'

export default function ScoreShareCard({ score = 742, category = 'Good', businessName = 'Your Business' }) {
  const [showShare, setShowShare] = useState(false)

  const shareUrl = `${window.location.origin}/shared-score/demo`

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl)
    toast.success('Share link copied!')
  }

  const handleDownloadPDF = () => {
    toast.success('Generating PDF report...')
    setTimeout(() => toast.success('PDF downloaded!'), 2000)
  }

  return (
    <>
      <button
        onClick={() => setShowShare(true)}
        className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 text-slate-700 text-sm font-medium hover:bg-slate-50 transition-colors"
      >
        <Share2 className="w-4 h-4" />
        Share Score
      </button>

      {showShare && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowShare(false)}>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="liquid-glass w-full max-w-sm p-6"
          >
            {/* Mini Score Card Preview */}
            <div className="gradient-primary rounded-2xl p-5 text-center mb-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(245,158,11,0.1),transparent_60%)]"></div>
              <p className="text-primary-200 text-xs font-medium relative">MSME Financial Health Score</p>
              <p className="text-4xl font-black text-white mt-2 relative">{score}</p>
              <p className="text-accent-400 text-sm font-bold mt-1 relative">{category}</p>
              <p className="text-primary-300 text-[11px] mt-2 relative">{businessName}</p>
            </div>

            <h3 className="font-semibold text-slate-800 mb-4">Share Your Score</h3>

            {/* Share Options */}
            <div className="space-y-2.5">
              <button
                onClick={handleCopyLink}
                className="w-full flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors text-left"
              >
                <div className="w-9 h-9 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Link2 className="w-4 h-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-800">Copy Share Link</p>
                  <p className="text-[11px] text-slate-400">Anyone with the link can view your score</p>
                </div>
                <Copy className="w-4 h-4 text-slate-400" />
              </button>

              <button
                onClick={handleDownloadPDF}
                className="w-full flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors text-left"
              >
                <div className="w-9 h-9 rounded-lg bg-emerald-50 flex items-center justify-center">
                  <Download className="w-4 h-4 text-emerald-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-800">Download PDF Report</p>
                  <p className="text-[11px] text-slate-400">Full health card with all dimensions</p>
                </div>
              </button>

              <button className="w-full flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors text-left">
                <div className="w-9 h-9 rounded-lg bg-violet-50 flex items-center justify-center">
                  <QrCode className="w-4 h-4 text-violet-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-800">Share via ULI</p>
                  <p className="text-[11px] text-slate-400">Send to lenders through Unified Lending Interface</p>
                </div>
              </button>
            </div>

            <p className="text-[10px] text-slate-400 text-center mt-4">
              Shared scores are read-only and expire after 30 days
            </p>
          </motion.div>
        </div>
      )}
    </>
  )
}
