import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Heart,
  Database,
  CreditCard,
  History,
  Building2,
  X,
  Activity,
  Sparkles,
} from 'lucide-react'

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/health-card', label: 'Health Card', icon: Heart },
  { path: '/data-connect', label: 'Data Sources', icon: Database },
  { path: '/credit-assessment', label: 'Credit Assessment', icon: CreditCard },
  { path: '/history', label: 'Score History', icon: History },
  { path: '/msme-register', label: 'Business Profile', icon: Building2 },
]

export default function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 left-0 h-full w-72 z-50 transform transition-transform duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 lg:static lg:z-auto`}
      >
        <div className="flex flex-col h-full gradient-primary relative overflow-hidden">
          {/* Decorative elements */}
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/[0.03] rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-20 left-0 w-32 h-32 bg-accent-500/[0.05] rounded-full -translate-x-1/2" />

          {/* Logo */}
          <div className="flex items-center justify-between p-5 relative">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-accent-400 to-accent-600 rounded-xl flex items-center justify-center shadow-lg shadow-accent-500/20">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-white font-bold text-sm leading-tight tracking-tight">MSME Health</h1>
                <p className="text-primary-300 text-[11px] font-medium">Score Platform</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-1.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto relative">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${
                    isActive
                      ? 'nav-active text-white'
                      : 'text-primary-200/80 hover:bg-white/[0.06] hover:text-white'
                  }`
                }
              >
                <item.icon className="w-[18px] h-[18px] flex-shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>

          {/* Upgrade card */}
          <div className="p-4 relative">
            <div className="bg-white/[0.06] backdrop-blur-sm rounded-2xl p-4 border border-white/[0.08]">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-accent-400" />
                <p className="text-white text-xs font-semibold">Powered by</p>
              </div>
              <p className="text-white text-sm font-bold">IDBI Bank</p>
              <p className="text-primary-300 text-[11px] mt-0.5">ULI • OCEN • Account Aggregator</p>
              <div className="mt-3 flex gap-1">
                <div className="h-1 flex-1 rounded-full bg-accent-500/60"></div>
                <div className="h-1 flex-1 rounded-full bg-emerald-500/60"></div>
                <div className="h-1 flex-1 rounded-full bg-blue-500/60"></div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
