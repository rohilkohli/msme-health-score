import { useState } from 'react'
import { Globe } from 'lucide-react'

export default function LanguageToggle() {
  const [lang, setLang] = useState('en')

  const toggle = () => {
    setLang(lang === 'en' ? 'hi' : 'en')
  }

  return (
    <button
      onClick={toggle}
      className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-sm"
      title={lang === 'en' ? 'Switch to Hindi' : 'Switch to English'}
    >
      <Globe className="w-4 h-4 text-slate-500" />
      <span className="text-xs font-bold text-slate-600 dark:text-slate-300">{lang === 'en' ? 'EN' : 'हिं'}</span>
    </button>
  )
}
