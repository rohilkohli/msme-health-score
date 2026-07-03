import { Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import MSMERegister from './pages/MSMERegister'
import DataConnect from './pages/DataConnect'
import HealthCard from './pages/HealthCard'
import CreditAssessment from './pages/CreditAssessment'
import History from './pages/History'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AnimatePresence mode="wait">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/msme-register" element={<MSMERegister />} />
          <Route path="/data-connect" element={<DataConnect />} />
          <Route path="/health-card" element={<HealthCard />} />
          <Route path="/credit-assessment" element={<CreditAssessment />} />
          <Route path="/history" element={<History />} />
        </Route>
      </Routes>
    </AnimatePresence>
  )
}

export default App
