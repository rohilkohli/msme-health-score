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
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-primary-800 dark:bg-slate-900 z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 lg:static lg:z-auto`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-4 border-b border-primary-700 dark:border-slate-700">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-accent-500 rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-white font-bold text-sm leading-tight">MSME Health</h1>
                <p className="text-primary-300 text-xs">Score Platform</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-1 rounded hover:bg-primary-700"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-accent-500 text-white shadow-md'
                      : 'text-primary-200 hover:bg-primary-700 hover:text-white'
                  }`
                }
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-primary-700 dark:border-slate-700">
            <div className="bg-primary-700/50 rounded-lg p-3">
              <p className="text-primary-200 text-xs font-medium mb-1">Powered by</p>
              <p className="text-white text-sm font-bold">IDBI Bank</p>
              <p className="text-primary-300 text-xs">ULI / OCEN / AA Framework</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
